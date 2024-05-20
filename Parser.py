from typing import List, Dict
from Token import Token, TokenType
from Logger import logger
import ASTNodes


class Parser:

    def __init__(self, lex_tokens:List[Token], gui):
        self.lex_tokens = lex_tokens
        self.gui = gui
        self.namespace:Dict[str,int|float|str] = {}
        self.var = None
        self.show_st = None
        self.operation = None
        self.statement = None
        self.loop = None
        logger.debug("Parser initialized with {} tokens".format(len(lex_tokens)))


    def parse(self):

        token_indx = 0
        while token_indx < len(self.lex_tokens):
            current_token = self.lex_tokens[token_indx]
            logger.debug(f"Processing token <{current_token.val}> of type <{current_token.token_type}>")

            if current_token.token_type == TokenType.KEYWORD:
                if current_token.val == 'dec':
                    self.var = ASTNodes.VariableDeclaration(self.lex_tokens, self.namespace, TokenType.IDENTIFIER, self.gui)
                    token_indx = self.var.parse_statement(token_indx)

                elif current_token.val == 'show' and token_indx != len(self.lex_tokens)-1 and self.lex_tokens[token_indx+1].val == '(':
                    self.show_st = ASTNodes.ShowStatement(self.lex_tokens, self.namespace, self.gui)
                    token_indx = self.show_st.parse_statement(token_indx)

                elif current_token.val == 'if' and token_indx != len(self.lex_tokens)-1 and self.lex_tokens[token_indx+1].val == '(':
                    self.statement = ASTNodes.Statement(self.lex_tokens, self.namespace, self.gui)
                    token_indx = self.statement.parse_statement(token_indx)

                elif current_token.val == 'while' and token_indx != len(self.lex_tokens)-1 and self.lex_tokens[token_indx+1].val == '(':
                    self.loop = ASTNodes.Loop(self.lex_tokens, self.namespace, self.gui)
                    token_indx = self.loop.parse_statement(token_indx)

            elif self.lex_tokens[token_indx].token_type == TokenType.IDENTIFIER and token_indx != len(self.lex_tokens)-1 and self.lex_tokens[token_indx+1].val == '=':
                self.operation = ASTNodes.Operation(self.lex_tokens, self.namespace, self.gui)
                token_indx = self.operation.parse_statement(token_indx)


            token_indx += 1

        logger.info("Parsing Completed.")





