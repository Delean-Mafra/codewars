class Phone:
    def __init__(self):
        self.ring = ""
        self.screen = ""
        self.microphone = ""
        self._current_contact = None

    def incomingcall(self, number_or_name):
        self._current_contact = None
        try:
            global contacts
            for c in contacts:
                if c.get('number') == number_or_name or c.get('name') == number_or_name:
                    self._current_contact = c
                    break
        except NameError:
            pass
        
        if self._current_contact:
            self.ring = self._current_contact.get('ring', 'Di Da Di')
            self.screen = f"Call: {self._current_contact.get('name', '')}\nNumber: {self._current_contact.get('number', '')}"
        else:
            self.ring = "Di Da Di"
            self.screen = f"Call: stranger\nNumber: {number_or_name}"   # <- corrigido aqui

    def connect(self):
        self.ring = ""
        self.screen = ""
        if self._current_contact:
            self.microphone = f"Hello, {self._current_contact.get('name', '')}!"
        else:
            self.microphone = "Hello, who is speaking, please?"

    def hangup(self):
        self.ring = ""
        self.screen = ""
        self.microphone = ""
        self._current_contact = None

    def __getattr__(self, name):
        return lambda *args, **kwargs: None
    
    
    
"""
████  █████ █     █████  ███  █   █    █   █  ███  █████ ████   ███  
█   █ █     █     █     █   █ ██  █    ██ ██ █   █ █     █   █ █   █ 
█   █ ████  █     ████  █████ █ █ █    █ █ █ █████ ████  ████  █████ 
█   █ █     █     █     █   █ █  ██    █   █ █   █ █     █  █  █   █ 
████  █████ █████ █████ █   █ █   █    █   █ █   █ █     █   █ █   █ 
"""
