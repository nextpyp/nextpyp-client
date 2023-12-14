
# this needs to be in its own module to avoid circular dependncies
# apparently the Python interpreter can't deal with those D=

class Credentials:

    def __init__(self, userid: str, token: str) -> None:
        self.userid = userid
        self.token = token
