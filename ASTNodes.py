from typing import List, Dict
import abc
from Token import Token, TokenType, Errors
from Logger import logger



class ASTNode(abc.ABC):

    def __init__(self, tokens:List[Token], namespace:Dict[str,None|str|int|float], gui):
        self.tokens = tokens
        self.namespace = namespace
        self.gui = gui
        logger.debug('ASTNode initialized with tokens and namespace.')


    @abc.abstractmethod
    def parse_statement(self, token_indx:int) -> int|None:
        ...


    def evaluate_expr(self,expression):
        try:
            new_val = eval(expression,self.namespace)
            logger.debug(f'Evaluating expression: {expression} = {new_val}')
            return new_val
        except Exception as e:
            self.gui.clear_display()
            self.gui.display_result_msg(f'{e}')

    def find_end_of_expr(self,token_indx:int):

        logger.info('Finding the end of expressions')
        current_index = token_indx
        while current_index < len(self.tokens):
            current_token = self.tokens[current_index]
            if current_token.val == '{':
                return current_index
            current_index += 1
        return current_index


    def find_end_of_op(self, start_index:int):

        current_index = start_index
        while current_index < len(self.tokens):
            current_token = self.tokens[current_index]

            if current_token.val == ';':
                return current_index

            elif current_token.token_type == TokenType.KEYWORD or (current_index != len(self.tokens)-1 and self.tokens[current_index+1].val in ['=','}']):
                logger.error('Missing a semicolon.')
                self.gui.clear_display()
                self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
                raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

            current_index += 1


class VariableDeclaration(ASTNode):

    def __init__(self, tokens, namespace, typee, gui):
        super().__init__(tokens, namespace, gui)
        self.typee = typee
        logger.debug('VariableDeclaration node created.')


    def parse_statement(self, token_indx) -> int|None:

        while token_indx < len(self.tokens):

            if self.tokens[token_indx].token_type == self.typee:
                if token_indx == len(self.tokens) - 1:
                    logger.error('Missing a semicolon.')
                    self.gui.clear_display()
                    self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
                    raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

                elif self.tokens[token_indx+1].val != ';' and self.tokens[token_indx+1].val != ',':
                    logger.error('Missing a semicolon.')
                    self.gui.clear_display()
                    self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
                    raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

                self.create_var(self.tokens[token_indx].val)
                logger.debug(f'Variable declared: {self.tokens[token_indx].val}')

            elif self.tokens[token_indx].val == ';':
                return token_indx

            token_indx += 1


    def create_var(self, variable_name:str):
        self.namespace[variable_name] = None

    def view_vars(self):
        print(self.namespace)
        logger.debug(f'Namespace contains: {self.namespace}')


class ShowStatement(ASTNode):


    def __init__(self, tokens, namespace, gui):
        super().__init__(tokens, namespace, gui)
        self.var = None
        logger.debug('ShowStatement node created.')



    def parse_statement(self, token_indx:int) -> int|None:

        holder = token_indx + 2
        while holder < len(self.tokens) and self.tokens[holder].val != ')':
            if self.tokens[holder].token_type == TokenType.COMMA and self.tokens[holder+1].val != ')':
                holder += 1
            self.var = self.tokens[holder]
            self.show_on_screen(self.var)
            holder += 1
        holder += 1
        if holder < len(self.tokens) and self.tokens[holder].val == ';':
            return holder
        logger.error('Missing a semicolon.')
        self.gui.clear_display()
        self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
        raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')


    def show_on_screen(self,var):

        if var.token_type == TokenType.NUMBER or var.token_type == TokenType.STRING:
            self.gui.display_result_msg(var.val)
            logger.info(f'Number/String shown on the screen as: {var.val}')
        elif var.token_type == TokenType.IDENTIFIER and var.val in self.namespace:
            self.gui.display_result_msg(self.namespace[var.val])
            logger.info(f'Valid Identifier shown on the screen as: {var.val}')
        else:
            self.gui.display_result_msg(f'{Errors.get(6)}: <{var.val}> is not defined')
            logger.error(f'Undefined Variable Error: <{var.val}> is not defined')
            raise Exception(f'{Errors.get(6)}: <{var.val}> is not defined')


class Operation(ASTNode):

    def __init__(self, tokens, namespace,gui):
        super().__init__(tokens, namespace, gui)
        self.op_expression = None
        logger.debug('Operation node created.')


    def parse_statement(self, token_indx:int) -> int|None:

        expr_start_index = token_indx + 2
        logger.debug(f'Operation start index at {expr_start_index}.')

        expr_end_index = self.find_end_of_op(expr_start_index)
        logger.debug(f'Operation end index at {expr_end_index}.')

        if expr_end_index is None:
            logger.error('Missing a semicolon.')
            self.gui.clear_display()
            self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
            raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        self.op_expression = "".join([token_ob.val for token_ob in expression_tokens_lst])
        logger.debug(f'Operation expression as a string -> {self.op_expression}.')

        new_val = self.evaluate_expr(self.op_expression)
        logger.debug(f'Evaluated expression -> {new_val}')

        if self.tokens[token_indx].val in self.namespace:
            self.namespace[self.tokens[token_indx].val] = new_val
            logger.info(f'{new_val} is added to namespace')
        return expr_end_index


class Statement(ASTNode):


    def __init__(self, tokens, namespace, gui):
        super().__init__(tokens, namespace, gui)
        self.expression = None
        logger.debug('Statement node created.')


    def parse_statement(self, token_indx:int) -> int|None:

        expr_start_index = token_indx + 1
        logger.debug(f'Condition start index at {expr_start_index}.')

        expr_end_index = self.find_end_of_expr(expr_start_index)
        logger.debug(f'Condition end index at {expr_end_index}.')

        if expr_end_index is None:
            logger.error('Missing a semicolon.')
            self.gui.clear_display()
            self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
            raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        expression = "".join([token_ob.val for token_ob in expression_tokens_lst])
        self.expression = self.evaluate_expr(expression)
        logger.debug(f'Evaluated expression -> {self.expression}')

        if self.expression:
            logger.info('Expression evaluated as True, executing true block.')
            token_indx = self.true_result(token_indx)
        else:
            logger.info('Expression evaluated as False, not executing the block.')
            token_indx = self.false_result(token_indx)
        return token_indx


    def true_result(self,index):

        current_index = index + 1
        logger.debug('Processing true result block.')

        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                current_index += 1
                while current_index < len(self.tokens) and self.tokens[current_index].val != '}':
                    current_token = self.tokens[current_index]
                    logger.info('Determining if nested statements exist')

                    if current_token.val in ['if','elif','else']:
                        current_index = self.parse_statement(current_index)

                    elif current_token.token_type == TokenType.KEYWORD:
                        logger.info('Determining the keyword operations')
                        if current_token.val == 'dec':
                            current_index = VariableDeclaration(self.tokens, self.namespace, TokenType.IDENTIFIER, self.gui).parse_statement(current_index)
                        elif current_token.val == 'show':
                            current_index = ShowStatement(self.tokens, self.namespace, self.gui).parse_statement(current_index)

                    elif current_token.token_type == TokenType.IDENTIFIER and current_index < len(self.tokens) - 1 and \
                            self.tokens[current_index + 1].val == '=':
                        logger.info('Determining the operations')
                        current_index = Operation(self.tokens, self.namespace, self.gui).parse_statement(current_index)
                    current_index += 1

                logger.info('Skipping through other blocks')
                skip = current_index+1
                while skip < len(self.tokens) and self.tokens[skip].val in ['elif','else']:
                    ignore_ind = skip
                    while ignore_ind < len(self.tokens) and self.tokens[ignore_ind].val != '}':
                        ignore_ind += 1
                    skip = ignore_ind+1
                    current_index = skip
                return current_index
            current_index += 1
        return index


    def false_result(self,index):
        current_index = index + 1
        logger.debug('Processing false statement.')

        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                logger.info('Determining curly braces')

                brace_count = 1
                current_index += 1
                while current_index < len(self.tokens) and brace_count > 0:
                    if self.tokens[current_index].val == '{':
                        brace_count += 1
                    elif self.tokens[current_index].val == '}':
                        brace_count -= 1
                    current_index += 1

                logger.info('Skipping through the current block')
                skip = current_index
                while skip < len(self.tokens) and self.tokens[skip].val in ['elif','else']:

                    logger.info('Determining if other statement blocks exist')
                    if self.tokens[skip].val == 'elif':
                        skip = self.parse_statement(skip)
                    elif self.tokens[skip].val == 'else':
                        self.true_result(skip)
                    ignore_ind = skip
                    while ignore_ind < len(self.tokens) and self.tokens[ignore_ind].val != '}':
                        ignore_ind += 1
                    skip = ignore_ind + 1
                    current_index = skip
                return current_index
            current_index += 1
        return index


class Loop(ASTNode):

    def __init__(self, tokens, namespace, gui):
        super().__init__(tokens, namespace, gui)
        self.loop_statement = None
        logger.debug('Loop node created.')


    def parse_statement(self, token_indx:int) -> int|None:

        expr_start_index = token_indx + 1
        logger.debug(f'Condition start index at {expr_start_index}.')

        expr_end_index = self.find_end_of_expr(expr_start_index)
        logger.debug(f'Condition end index at {expr_end_index}.')

        if expr_end_index is None:
            logger.error('Missing a semicolon.')
            self.gui.clear_display()
            self.gui.display_result_msg(f'{Errors.get(5)}: Oops! missed semicolon.')
            raise Exception(f'{Errors.get(5)}: Oops! missed semicolon.')

        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        expression = "".join([token_ob.val for token_ob in expression_tokens_lst])

        while True:
            self.loop_statement = self.evaluate_expr(expression)
            logger.debug(f'Evaluated expression -> {self.loop_statement}')

            if self.loop_statement:
                logger.info('Expression evaluated as True, executing the block.')
                token_indx = self.true_statement(token_indx)
            else:
                logger.info('Expression evaluated as False, stopping the execution of the block.')
                token_indx = self.false_statement(token_indx)
                break
        return token_indx


    def true_statement(self, index):

        current_index = index + 1
        logger.debug('Processing the block.')

        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                current_index += 1
                while current_index < len(self.tokens) and self.tokens[current_index].val != '}':
                    current_token = self.tokens[current_index]
                    logger.info('Determining if nested statements exist')

                    if current_token.val in ['if', 'elif', 'else']:
                        current_index = Statement(self.tokens,self.namespace,self.gui).parse_statement(current_index)
                        return index

                    elif current_token.val == 'while':
                        logger.info('Determining if nested loops exist')
                        current_index = self.parse_statement(current_index)

                    elif current_token.token_type == TokenType.KEYWORD:

                        logger.info('Determining the keyword operations')
                        if current_token.val == 'dec':
                            current_index = VariableDeclaration(self.tokens, self.namespace, TokenType.IDENTIFIER, self.gui).parse_statement(
                                current_index)
                        elif current_token.val == 'show':
                            current_index = ShowStatement(self.tokens, self.namespace, self.gui).parse_statement(current_index)

                    elif current_token.token_type == TokenType.IDENTIFIER and current_index < len(self.tokens) - 1 and self.tokens[current_index + 1].val == '=':
                        logger.info('Determining the operations')
                        current_index = Operation(self.tokens, self.namespace, self.gui).parse_statement(current_index)

                    current_index += 1
                current_index = index
                return current_index
            current_index += 1
        return index


    def false_statement(self,index):
        current_index = index + 1
        logger.debug('Processing false condition.')

        while current_index < len(self.tokens):

            logger.info('Determining curly braces')
            if self.tokens[current_index].val == '{':
                brace_count = 1
                current_index += 1

                logger.info('Skipping through the current block')
                while current_index < len(self.tokens) and brace_count > 0:
                    if self.tokens[current_index].val == '{':
                        brace_count += 1
                    elif self.tokens[current_index].val == '}':
                        brace_count -= 1
                    current_index += 1

                return current_index-1
            current_index += 1
        return index