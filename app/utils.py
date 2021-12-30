import passlib
from passlib import context
from passlib.context import CryptContext

d = CryptContext(schemes=["bcrypt"], deprecated="auto")


def func(plain_pass):
    return d.hash(plain_pass)


def AuthRequest(plain, hash):
    return d.verify(plain, hash)
