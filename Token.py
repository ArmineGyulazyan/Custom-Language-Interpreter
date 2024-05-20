from enum import Enum

Errors = {1:'Invalid Token Error.',  #first 4 -> lexer error
          2:'Nested Comment Block Error.',
          3:'Unopened Comment Block Closed Error',
          4:'Unterminated Comment Block Error',
          5:'Semicolon Missing Error', #from 5 to 7 parser errors
          6:'Undefined Variable Error',
          7:'Failed to Clear the Log File', #from 7 -> errors that Python may raise
          }

class TokenType(Enum):

    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    PARENTHESIS = 'PARENTHESIS'
    COMMA = 'COMMA'
    OPERATOR = 'OPERATOR'
    SEMICOLON = 'SEMICOLON'

class Token:

    def __init__(self, token_type:TokenType, val:str):

        self.token_type = token_type
        self.val = val



