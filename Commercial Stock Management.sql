/*  
████████    ██      ██  
████████    ██      ██  
██      ██  ████  ████  
██      ██  ████  ████  
██      ██  ██  ██  ██  
██      ██  ██  ██  ██  
██      ██  ██      ██  
██      ██  ██      ██  
████████    ██      ██  
████████    ██      ██  
*/

WITH dates AS (
    SELECT product_id, '2000-01-01'::date as d FROM products
    UNION
    SELECT product_id, '2025-01-01'::date as d FROM products
    UNION
    SELECT product_id, valid_from FROM product_versions WHERE valid_from > '2000-01-01' AND valid_from < '2025-01-01'
    UNION
    SELECT product_id, valid_to FROM product_versions WHERE valid_to > '2000-01-01' AND valid_to < '2025-01-01'
    UNION
    SELECT s.product_id, slv.valid_from
    FROM stocks s
    JOIN stock_levels sl USING (stock_id)
    JOIN stock_level_versions slv USING (stock_level_id)
    WHERE slv.valid_from > '2000-01-01' AND slv.valid_from < '2025-01-01'
    UNION
    SELECT s.product_id, slv.valid_to
    FROM stocks s
    JOIN stock_levels sl USING (stock_id)
    JOIN stock_level_versions slv USING (stock_level_id)
    WHERE slv.valid_to > '2000-01-01' AND slv.valid_to < '2025-01-01'
),
periods AS (
    SELECT
        product_id,
        d as valid_from,
        LEAD(d) OVER (PARTITION BY product_id ORDER BY d) as valid_to
    FROM dates
),
valid_periods AS (
    SELECT product_id, valid_from, valid_to
    FROM periods
    WHERE valid_to IS NOT NULL AND valid_from < valid_to
),
period_amounts AS (
    SELECT
        p.product_id,
        p.valid_from,
        p.valid_to,
        prod_status.status,
        stock_data.amt_commercial,
        stock_data.amt_additional,
        stock_data.amt_published,
        stock_data.amt_booked
    FROM valid_periods p
    LEFT JOIN LATERAL (
        SELECT status
        FROM product_versions pv
        WHERE pv.product_id = p.product_id
          AND pv.valid_from <= p.valid_from
          AND pv.valid_to >= p.valid_to
        LIMIT 1
    ) prod_status ON true
    LEFT JOIN LATERAL (
        SELECT
            MAX(CASE WHEN sl.kind = 'commercial' THEN slv.amount END) AS amt_commercial,
            MAX(CASE WHEN sl.kind = 'additional' THEN slv.amount END) AS amt_additional,
            MAX(CASE WHEN sl.kind = 'published' THEN slv.amount END) AS amt_published,
            SUM(CASE WHEN sl.kind = 'booked' THEN slv.amount END) AS amt_booked
        FROM stocks s
        JOIN stock_levels sl USING (stock_id)
        JOIN stock_level_versions slv USING (stock_level_id)
        WHERE s.product_id = p.product_id
          AND slv.valid_from <= p.valid_from
          AND slv.valid_to >= p.valid_to
    ) stock_data ON true
),
calculated_amounts AS (
    SELECT
        product_id,
        valid_from,
        valid_to,
        CASE
            WHEN status IS NULL OR status = 'closed' THEN 0
            ELSE GREATEST(0,
                (CASE
                    WHEN amt_published IS NULL THEN COALESCE(amt_commercial, 0) + COALESCE(amt_additional, 0)
                    ELSE LEAST(COALESCE(amt_commercial, 0) + COALESCE(amt_additional, 0), amt_published)
                END) - COALESCE(amt_booked, 0)
            )
        END::bigint AS available_amount
    FROM period_amounts
),
grouped AS (
    SELECT
        product_id,
        valid_from,
        valid_to,
        available_amount,
        SUM(CASE WHEN prev_amount = available_amount THEN 0 ELSE 1 END)
            OVER (PARTITION BY product_id ORDER BY valid_from) AS grp
    FROM (
        SELECT
            product_id,
            valid_from,
            valid_to,
            available_amount,
            LAG(available_amount) OVER (PARTITION BY product_id ORDER BY valid_from) AS prev_amount
        FROM calculated_amounts
    ) t
),
merged AS (
    SELECT
        product_id,
        MIN(valid_from) AS valid_from,
        MAX(valid_to) AS valid_to,
        available_amount
    FROM grouped
    GROUP BY product_id, grp, available_amount
),
final_output AS (
    SELECT
        pr.name AS product_name,
        m.valid_from,
        m.valid_to,
        m.available_amount,
        s.standard_unit AS available_unit,
        COUNT(*) OVER (PARTITION BY m.product_id) AS record_count
    FROM merged m
    JOIN products pr ON pr.product_id = m.product_id
    LEFT JOIN stocks s ON s.product_id = m.product_id
)
SELECT
    product_name,
    valid_from,
    valid_to,
    available_amount,
    available_unit
FROM final_output
ORDER BY record_count ASC, product_name ASC, valid_from ASC;


/* 
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                       .::.                                     
                               ..=*##%%%###*++=-::......      ....:                                                .+@@@###@+                                   
                           .*%@@@@%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@=                                              .#@@%:    -%*                                  
                         -%@%=.    :=+:      :#@%*+*##%#%###*+-:.                                .              +@@@=      +@*                                  
                       .#@%:     -*-:#@+   -%@@+     -##+                                    -#@@@@@%*-       .*@@%:     .*@%:                                  
                       =@@=         -@#. .%@@%:    .#@*.*                                    .    .=*%@@*:   .%@@#.    .+@@#.                                   
                       :%@%-.   ..=@%:  :%@@%.    .%@+ :+                                              -#%@#=%@@%.  .:#@%*       .%%.                           
                         .+%@@@@%*:    =@@@*.    -@@-.*+                                                  .+@@@@@%%%#+:  =%#.   -%%-                            
                                      =@@@#     =@@*#*.                                                   =@@@*        :%@%:   +@%.                             
                   .=#@%%%%+.        +@@@+   :#%@%=--.        ..    ..      :=-.                         =@@@+         :-.   .*@#.    .--.                      
                  *@#:     :*.      *@@@+    .*@@%%@@%:     :%@=   +@%.  .*@%#%@=+@#.                   +@@@=        =@%.   .#@*   .+@%#%@*.                    
                .#@-              .#@@@-    .%@*.  *@%.    =@%:  .#@*.  +@%.   #@@#                    *@@@:       .*@*.   :%@=   +@%:  .%+                     
                :@#.             :%@@@:    :%%-   =@@:    +%%.  .@@=  .#@*.   :%@+                   .%@@%:       .%@+    -@@-  .#@+  .+%=                      
                :%%.           .#@@@+     -%%:  .#@*. .  #@*   +@%-  .+@@-   .%@=  .                -%@@*        :%@=  ..+@#.  .=@%+++-:   .                    
                 :%%+.      .=%@@%+.     +@#.  :%@*-*%=.*@*:+%%@@-=#%=*@@#--*@%:-*@+.    -##*++*#%@@@@@*:       .%@=-*%*%@%-+%#:+@@#-:::=*%*.                   
                   -#%@@%%@@@%#+.       =#+   .#%#*:   :##*=. +##*-   .+###%@@%*-.      .#%:   .:+%@#=*%@@@#=:  =##*- .%@#*+:    -#%%##+:                       
                                                                       .#%@@+             .+#%%%#*:      .+%@@@@%=.  .%@=:-                                     
                                                                      #- #@+                                 .+%@@@@@@@+.*.             .=+                     
                                                                    -* -@@-                                      :=%@@@@@@@@%%%######%@%+.                      
                                                                   .+.=@%:                                        *@*.++-=+**###*++=:.                          
                                                                   -##@+                                         -@@#*.                                         
                                                                    --                                                                                          
                                                                                                                                                                
                                                               -###%+++************++=:.                                                                        
                                                           .=*##############################*=-.                                                                
                                                       .=*#####################################%##=.                                                            
                                                    .=*#############%%%################%%##%%%%##=*#=                                                           
                                                  -##########%#%%%%%%%#################%###%%%%%#%*+%=                                                          
                                               .*###########%%#%%%%%%%###############%%%%%%%%%%%%%#*+#-                                                         
                                             -*######%#####%#%######%%%#############%%%%%%%%%%%%%%%*+*#:                                                        
                                           =########%%#######%####################%%%%%%%%%%%%%%%%%%%***.                                                       
                                         -###################%############%%###%%%%#%#######-#%%%%%%%%*#+                                                       
                                        =#####################%#########%%%%%%%%%%%%%-=====*%%%%%%%%%%%#*.                                                      
                       ..              =####################+*%#%%%%%%%%%%%%%+:=+#%*==*%%%==#%%%%%%%%%##%#.                                                     
                      .#%*-.        ..-################%#++:=%%%%%%%%%%+:-+%#+:=+%%%+=+*%%#=+#%%%%%%%%%%%%*          .--=+****=:                                
                      .#%%%*-..:-=--==*###########**#**=+%+::#%%%==*%%*-..+%%%=.-#%%%+==#%%+=+#%%%%%%%%%%%%%-:-+#***#*#########=                                
                       +%%%%##==******#######-. ......:+%#*-.+%*+=--=#%%=..*%%#:.=%%%%=====+%+=+#%%%%%%%%%%%%#################-                                 
                       :#%%%%%%*+:    *####-:*=#+::#+*%%%%**:.+%%%+::*%%%=..#%%*..+%%%%%%#=#%%#*+%%%%%%%%%%#%#=:.    .:#####:                                   
                        -%#######*=:. +###:#%=*%*-:*%=%%%%%%+:.#%%%-:.#%%#=:-%*#*-=*%%%%%---+##%%%%%%%%%%%%#=.     .+##%#-                                      
                         =%%%%%###**=-=#%##%*-*%#=.+%*#%%%%%#=.-#%%#:.-%%%#+=*%%%%%%%%%%#+#%%%%%%%%%%%%%%###*=-=*#%##+:      .:::.                              
                         .+%%%%*##*#*==#%%%%*=+%#=:-%*#%%%#%%#-.+%%%+.-#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%*=      .=*#%%%@@:                             
                          .#%%#*+***#*=+%%%%#=+%#=.+%#=%%%-#%%-..+%%+-*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%+:-+#@@@@@@@@@%#%%%@#.                            
                           .#%%##**###*=*%%%%+-=*-####=%+:*%%%%%*%%:+%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%@%%*##%#*+*#@%#:-%####%#.                            
                            .*######%##*+#%%%#==-:------*%%%%%%%*+#%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*%##**+####+#*%##*#@@%####%=                             
                              +%#**#****+*%%%%%******##%%%%%%%%#%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#***##%****##*==*%****#@%####*:                              
                               :**++###***##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%@@%##*=--+-#**##**=-+#+=-*#*%%#%%*:                               
                                 .=**%%**+##%%%%%%%%%%%%%#%%%%%%#%######%*+##%#+#*+%%@%%%%%%%%@%%%*+#*:*-=*##=-+%-*#+-+**+#%%#=                                 
                                   .-+*#%%#%%%#%#%%%%%%%%###+*+%##*#**%##+**#%##++%#%%%%%%#+*#%%%+***+-+==***+-*#=*+#==*+#%%*.                                  
                                      -**#%%%%==*%%%#*#+#%#*#*##***#*#*##*#+*%#==-=-=@%%*=====+%%@***#+=+*++++--+*=+#+*+%#@+                                    
                                       .-+*#%%@@@@@%%+=-:=:-+***-=**-**+:++*:+#--#*:*%%%===+++==#@%*#**=+++=+*#+**##+**#*#@.                                    
                                          :+*##%@@@#=++=-#*+#***+-=*+-*#--#+-=*+:**--%%#===++++++=%%%#+##*+#*#***##+**##%+                                      
                                            .*###%@@#=*#:=##**#+#-+=*:=%%:-+=:+=*+#*#%%==+*++=======%%%#****#*=#%#+#%%#.                                        
                                              :#*#%%%-*#=+**%+-##+:**=-##**+####=*%#%%*++*+==**+*+*+=--*%%%@%@@@%*-.                                            
                                             .=+***#%#-:-=+-=*#*+%#*+*+#%**+*%*+*#*%%#****+===++*#%@@#=--:**:.                                                  
                                            .-==++***%%#****##*****%***##*+##*#**%%#****#####*+==-===--:-:::--:                                                 
                                            :-===++***%@%**####**#*#***#**#*#%#@%###*******####**+=====-------:.                                                
                                            --=====++=++%@%%#*%+**#*#**#%%@%%%###**++++++********+++++==-=--=--:                                                
                                           .-====+++=+++++***#%%%%%###+++#%%%###+++==+++++**#***+==+++===+======:                                               
                                            -===+++==+++****+++**+++===++**####**##**+++************#+=-+*++=+===.                                              
                                            -==++++++++****+++***+++==+++*******#%########%%%#+#-+::*....=--+#++=                                               
                                            -=+++++++******+*+***+*+++++++***+**######****++**++===---::::-+=--=-                                               
                                            :=+++++++*******++**+++*++++**+*******##*+++**********++++==--===*+=--:                                             
                                            :=++++++***##***+********+***+*+***+*****++*######**#**#***##**+===+*==---.                                         
                                            .=+++*****###***+************++****++**#**+*#####%######******+=+==. -*+=--:::                                      
                                             -+++****#####****************+**+++++**##**####%#%%%%#%#%******+*=.   -*+==---::.                                  
                                             -++*****#####*********#***+*+***+++++***#####%%%%%%%@@%%%%%%%##*+:      :**+===-:-:.                               
                                             -+++****#***#******###**********+++++**#*####%#%%%%%%#******%#*-.         .***+==+*##*-                            
                                             :+*+*************###*************++*****#*#*########%%#%###*+=.             .+#**#%%%%##=                          
                                             -+****++*********######********#******##*##*###%%%%%%%%##*=-:                 .=%%%@%#*+++                         
                                             -+****************######*****#####****#%#*##*##%%%%%##*++==.                    .=%@*++=*=                         
                                             -++**************#######****###########%#######%%%%##++*+=.                        -%###-                          
                                            .+******++*********##################%#%%#%%###%%%##***++=.                                                         
                                            :+****##************###############%%%%%%%%%%%%%%%%##***=:                                                          
                                            :+*****##***********###*###########%%%%%%%%%%%%%%%%#**+=.                                                           
                                            -****#*#*********#**##*###########%%%%%%%%%%%%%%%##**+-.                                                            
                                           .=*****#******###################%%%%%%@%%%%########+-                                                               
                                           :+*##**********#####%#%###%%%%%%@%@%@@@@@%%##%###*+:                                                                 

*/


