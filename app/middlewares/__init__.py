from .access_function import AccessFunction
from .access_sub import SubVerify

middlewares = [
    AccessFunction(),
    SubVerify()
]