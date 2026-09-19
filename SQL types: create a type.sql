DROP TYPE IF EXISTS rational CASCADE;

CREATE TYPE rational AS (
    num numeric,
    den numeric
);

CREATE OR REPLACE FUNCTION dm_gcd(dm numeric, dm1 numeric) RETURNS numeric AS $$
DECLARE
    dm2 numeric;
BEGIN
    WHILE dm1 <> 0 LOOP
        dm2 := dm1;
        dm1 := mod(dm, dm1);
        dm := dm2;
    END LOOP;
    RETURN abs(dm);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION rational(dm numeric, dm1 numeric) RETURNS rational AS $$
DECLARE
    dm2 numeric;
    dm3 rational;
BEGIN
    IF dm1 = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;
    dm := trunc(dm);
    dm1 := trunc(dm1);
    IF dm1 < 0 THEN
        dm := -dm;
        dm1 := -dm1;
    END IF;
    dm2 := dm_gcd(abs(dm), abs(dm1));
    IF dm2 = 0 THEN
        dm2 := 1;
    END IF;
    dm3.num := trunc(dm / dm2);
    dm3.den := trunc(dm1 / dm2);
    RETURN dm3;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION rational(dm integer, dm1 integer) RETURNS rational AS $$
BEGIN
    RETURN rational(dm::numeric, dm1::numeric);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION rational(dm bigint, dm1 bigint) RETURNS rational AS $$
BEGIN
    RETURN rational(dm::numeric, dm1::numeric);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_text_to_rational(dm text) RETURNS rational AS $$
DECLARE
    dm1 text;
    dm2 text[];
    dm3 numeric;
    dm4 numeric;
BEGIN
    dm := trim(dm);
    IF dm LIKE '(%,' OR dm LIKE '(%,%' THEN
        dm1 := trim(both '()' from dm);
        dm2 := string_to_array(dm1, ',');
        dm3 := trim(dm2[1])::numeric;
        dm4 := trim(dm2[2])::numeric;
    ELSIF dm LIKE '%/%' THEN
        dm2 := string_to_array(dm, '/');
        dm3 := trim(dm2[1])::numeric;
        dm4 := trim(dm2[2])::numeric;
    ELSE
        dm3 := dm::numeric;
        dm4 := 1;
    END IF;
    RETURN rational(dm3, dm4);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_varchar_to_rational(dm varchar) RETURNS rational AS $$
BEGIN
    RETURN dm_text_to_rational(dm::text);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE CAST (text AS rational) WITH FUNCTION dm_text_to_rational(text) AS IMPLICIT;
CREATE CAST (varchar AS rational) WITH FUNCTION dm_varchar_to_rational(varchar) AS IMPLICIT;

CREATE OR REPLACE FUNCTION dm_rational_to_text(dm rational) RETURNS text AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    IF dm.den = 1 THEN
        RETURN dm.num::text;
    ELSE
        RETURN dm.num::text || '/' || dm.den::text;
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_rational_to_varchar(dm rational) RETURNS varchar AS $$
BEGIN
    RETURN dm_rational_to_text(dm)::varchar;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE CAST (rational AS text) WITH FUNCTION dm_rational_to_text(rational) AS ASSIGNMENT;
CREATE CAST (rational AS varchar) WITH FUNCTION dm_rational_to_varchar(rational) AS ASSIGNMENT;

CREATE OR REPLACE FUNCTION dm_numeric_to_rational(dm numeric) RETURNS rational AS $$
DECLARE
    dm1 text;
    dm2 text[];
    dm3 int;
    dm4 numeric;
    dm5 numeric;
BEGIN
    dm1 := trim_scale(dm)::text;
    IF position('.' in dm1) > 0 THEN
        dm2 := string_to_array(dm1, '.');
        dm3 := length(dm2[2]);
        dm5 := power(10, dm3);
        dm4 := trunc(dm * dm5);
        RETURN rational(dm4, dm5);
    ELSE
        RETURN rational(trunc(dm), 1);
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_integer_to_rational(dm integer) RETURNS rational AS $$
BEGIN
    RETURN rational(dm::numeric, 1::numeric);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_bigint_to_rational(dm bigint) RETURNS rational AS $$
BEGIN
    RETURN rational(dm::numeric, 1::numeric);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE CAST (numeric AS rational) WITH FUNCTION dm_numeric_to_rational(numeric) AS IMPLICIT;
CREATE CAST (integer AS rational) WITH FUNCTION dm_integer_to_rational(integer) AS IMPLICIT;
CREATE CAST (bigint AS rational) WITH FUNCTION dm_bigint_to_rational(bigint) AS IMPLICIT;

CREATE OR REPLACE FUNCTION dm_rational_to_numeric(dm rational) RETURNS numeric AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    RETURN dm.num / dm.den;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_rational_to_bigint(dm rational) RETURNS bigint AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    RETURN trunc(dm.num / dm.den)::bigint;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_rational_to_integer(dm rational) RETURNS integer AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    RETURN trunc(dm.num / dm.den)::integer;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE CAST (rational AS numeric) WITH FUNCTION dm_rational_to_numeric(rational) AS ASSIGNMENT;
CREATE CAST (rational AS bigint) WITH FUNCTION dm_rational_to_bigint(rational) AS ASSIGNMENT;
CREATE CAST (rational AS integer) WITH FUNCTION dm_rational_to_integer(rational) AS ASSIGNMENT;

CREATE OR REPLACE FUNCTION dm_add(dm rational, dm1 rational) RETURNS rational AS $$
BEGIN
    RETURN rational(dm.num * dm1.den + dm1.num * dm.den, dm.den * dm1.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_sub(dm rational, dm1 rational) RETURNS rational AS $$
BEGIN
    RETURN rational(dm.num * dm1.den - dm1.num * dm.den, dm.den * dm1.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_neg(dm rational) RETURNS rational AS $$
BEGIN
    RETURN rational(-dm.num, dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_mul(dm rational, dm1 rational) RETURNS rational AS $$
BEGIN
    RETURN rational(dm.num * dm1.num, dm.den * dm1.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_div(dm rational, dm1 rational) RETURNS rational AS $$
BEGIN
    RETURN rational(dm.num * dm1.den, dm.den * dm1.num);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_mod(dm rational, dm1 rational) RETURNS rational AS $$
DECLARE
    dm2 numeric;
    dm3 numeric;
    dm_res rational;
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    dm2 := (dm.num * dm1.den) / (dm.den * dm1.num);
    dm3 := trunc(dm2);
    dm_res := rational(dm3, 1::numeric);
    RETURN dm_sub(dm, dm_mul(dm_res, dm1));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OPERATOR + (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_add);
CREATE OPERATOR - (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_sub);
CREATE OPERATOR - (RIGHTARG = rational, PROCEDURE = dm_neg);
CREATE OPERATOR * (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_mul);
CREATE OPERATOR / (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_div);
CREATE OPERATOR % (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_mod);

CREATE OR REPLACE FUNCTION dm_eq(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) = (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_ne(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) <> (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_lt(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) < (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_le(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) <= (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_gt(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) > (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION dm_ge(dm rational, dm1 rational) RETURNS boolean AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    dm1 := rational(dm1.num, dm1.den);
    RETURN (dm.num * dm1.den) >= (dm1.num * dm.den);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OPERATOR = (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_eq, COMMUTATOR = =);
CREATE OPERATOR <> (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_ne, COMMUTATOR = <>);
CREATE OPERATOR < (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_lt, COMMUTATOR = >);
CREATE OPERATOR <= (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_le, COMMUTATOR = >=);
CREATE OPERATOR > (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_gt, COMMUTATOR = <);
CREATE OPERATOR >= (LEFTARG = rational, RIGHTARG = rational, PROCEDURE = dm_ge, COMMUTATOR = <=);

CREATE OR REPLACE FUNCTION numerator(dm rational) RETURNS numeric AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    RETURN dm.num;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION denominator(dm rational) RETURNS numeric AS $$
BEGIN
    dm := rational(dm.num, dm.den);
    RETURN dm.den;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OPERATOR ?/- (RIGHTARG = rational, PROCEDURE = numerator);
CREATE OPERATOR -/? (RIGHTARG = rational, PROCEDURE = denominator);
