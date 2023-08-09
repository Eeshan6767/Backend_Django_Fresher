class UserAlreadyExists(Exception) :  
    def __init__(self, msg) :
        self.message = msg
        super().__init__(msg)


class Wrong_HTTP_Method(Exception):
    def __init__(self, msg) :
        self.message = msg
        super().__init__(msg)


class Bad_JSON_Body(Exception) :
    def __init__(self, msg) :
        self.message = msg
        super().__init__(msg)

class JSON_Decode_Error(Exception) :
    def __init__(self, msg) :
        self.message = msg
        super().__init__(msg)