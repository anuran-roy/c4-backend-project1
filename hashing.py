from passlib.context import CryptContext

class Hash():
    def bcrypt(self, password):
        pwd_cxt = CryptContext(schemes = ['bcrypt'], deprecated='auto')