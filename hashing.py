from passlib.context import CryptContext

class Hash():
    def bcrypt(self, password: str):
        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Making Password Context
        return pwd_cxt.hash(password)
