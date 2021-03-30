

class APIPermission(object):
    def __init__(self, client_key: str):
        keys = client_key.split(':')
        self.CLIENT_ID = keys[0]
        self.CLIENT_SECRET = keys[1]
        self.CLIENT_SCOPE = {}
        

 