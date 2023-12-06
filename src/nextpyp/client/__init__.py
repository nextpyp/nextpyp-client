

class Credentials:
    def __init__(self, userid: str, token: str):
        self.userid = userid
        self.token = token


class Client:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
