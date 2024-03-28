from enum import Enum

class TokenType(Enum):

    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    PARENTHESIS = 'PARENTHESIS'
    COMMA = 'COMMA'
    OPERATOR = 'OPERATOR'

class Token:

    def __init__(self, token_type:TokenType, val:str):

        self.token_type = token_type
        self.val = val
        #self.line = line


