from typing import List, Dict, Optional
import abc
from Token import Token, TokenType



class ASTNode(abc.ABC):

    def __init__(self, tokens:List[Token], namespace:Dict[str,None|str|int|float], gui):
        self.tokens = tokens
        self.namespace = namespace
        self.gui = gui

    @abc.abstractmethod
    def parse_statement(self, token_indx:int) -> Optional[int]:
        ...

    def evaluate_expr(self,expression):
        new_val = eval(expression,self.namespace)
        return new_val

    def find_end_of_expr(self,token_indx:int):

        current_index = token_indx
        while current_index < len(self.tokens):
            current_token = self.tokens[current_index]
            if current_token.val == '{':
                return current_index
            current_index += 1
        return current_index

    def find_end_of_op(self,start_index:int):

        current_index = start_index
        while current_index < len(self.tokens):
            current_token = self.tokens[current_index]

            if current_token.token_type == TokenType.KEYWORD:
                return current_index

            elif current_token.token_type == TokenType.IDENTIFIER:
                if current_index + 1 < len(self.tokens) and self.tokens[current_index + 1].val == '=':
                    return current_index
            elif current_token.val == '}':
                return current_index
            current_index += 1
        return current_index

class VariableDeclaration(ASTNode):

    def __init__(self, tokens, namespace, typee, gui):
        super().__init__(tokens, namespace, gui)
        self.typee = typee

    def parse_statement(self, token_indx) -> Optional[int]:

        while token_indx < len(self.tokens):
            if self.tokens[token_indx+1].token_type == self.typee:
                self.create_var(self.tokens[token_indx+1].val)
                break

    def create_var(self, variable_name:str):
        self.namespace[variable_name] = None

    def view_vars(self):
        print(self.namespace)


class ShowStatement(ASTNode):

    def __init__(self, tokens, namespace, gui):
        super().__init__(tokens, namespace, gui)
        self.var = None

    def parse_statement(self, token_indx:int) -> Optional[int]:

        holder = token_indx + 2
        while holder < len(self.tokens) and self.tokens[holder].val != ')':
            if self.tokens[holder].token_type == TokenType.COMMA and self.tokens[holder+1].val != ')':
                holder += 1
            self.var = self.tokens[holder]
            self.show_on_screen(self.var)
            holder += 1

    def show_on_screen(self,var):

        if var.token_type == TokenType.NUMBER or var.token_type == TokenType.STRING:
            self.gui.display_result_msg(var.val)
            # print(var.val)
        elif var.token_type == TokenType.IDENTIFIER and var.val in self.namespace:
            self.gui.display_result_msg(self.namespace[var.val])
            # print(self.namespace[var.val])
        else:
            self.gui.display_result_msg(f'NameERROR: {var.val} is not defined')
            # print(f'NameERROR: {var.val} is not defined')


class Operation(ASTNode):

    def __init__(self, tokens, namespace,gui):
        super().__init__(tokens, namespace, gui)
        self.op_expression = None


    def parse_statement(self, token_indx:int) -> Optional[int]:

        expr_start_index = token_indx + 2
        expr_end_index = self.find_end_of_op(expr_start_index)
        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        self.op_expression = "".join([token_ob.val for token_ob in expression_tokens_lst])
        new_val = self.evaluate_expr(self.op_expression)
        if self.tokens[token_indx].val in self.namespace:
            self.namespace[self.tokens[token_indx].val] = new_val



class Statement(ASTNode):

    def __init__(self, tokens, namespace, gui):
        super().__init__(tokens, namespace, gui)
        self.expression = None

    def parse_statement(self, token_indx:int) -> Optional[int]:

        expr_start_index = token_indx + 1
        expr_end_index = self.find_end_of_expr(expr_start_index)
        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        expression = "".join([token_ob.val for token_ob in expression_tokens_lst])
        self.expression = self.evaluate_expr(expression)

        if self.expression:
            token_indx = self.true_result(token_indx)
        else:
            token_indx = self.false_result(token_indx)
        return token_indx

    def true_result(self,index):

        current_index = index + 1
        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                current_index += 1
                while current_index < len(self.tokens) and self.tokens[current_index].val != '}':
                    current_token = self.tokens[current_index]
                    if current_token.val in ['if','elif','else']:
                        current_index = self.parse_statement(current_index)
                    elif current_token.token_type == TokenType.KEYWORD:
                        if current_token.val == 'dec':
                            VariableDeclaration(self.tokens, self.namespace, TokenType.IDENTIFIER, self.gui).parse_statement(current_index)
                        elif current_token.val == 'show':
                            ShowStatement(self.tokens, self.namespace, self.gui).parse_statement(current_index)
                    elif current_token.token_type == TokenType.IDENTIFIER and current_index < len(self.tokens) - 1 and \
                            self.tokens[current_index + 1].val == '=':
                        Operation(self.tokens, self.namespace, self.gui).parse_statement(current_index)
                    current_index += 1

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
        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                brace_count = 1
                current_index += 1
                while current_index < len(self.tokens) and brace_count > 0:
                    if self.tokens[current_index].val == '{':
                        brace_count += 1
                    elif self.tokens[current_index].val == '}':
                        brace_count -= 1
                    current_index += 1
                skip = current_index
                while skip < len(self.tokens) and self.tokens[skip].val in ['elif','else']:
                    if self.tokens[skip].val == 'elif':
                        self.parse_statement(skip)
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

    def parse_statement(self, token_indx:int) -> Optional[int]:

        expr_start_index = token_indx + 1
        expr_end_index = self.find_end_of_expr(expr_start_index)
        expression_tokens_lst = self.tokens[expr_start_index:expr_end_index]
        expression = "".join([token_ob.val for token_ob in expression_tokens_lst])

        while True:
            self.loop_statement = self.evaluate_expr(expression)
            if self.loop_statement:
                token_indx = self.true_statement(token_indx)
            else:
                token_indx = self.false_statement(token_indx)
                break
        return token_indx

    def true_statement(self, index):

        current_index = index + 1
        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                current_index += 1
                while current_index < len(self.tokens) and self.tokens[current_index].val != '}':
                    current_token = self.tokens[current_index]
                    if current_token.val in ['if', 'elif', 'else']:
                        current_index = Statement(self.tokens,self.namespace).parse_statement(current_index)
                        return index
                    elif current_token.val == 'while':
                        current_index = self.parse_statement(current_index)
                    elif current_token.token_type == TokenType.KEYWORD:
                        if current_token.val == 'dec':
                            VariableDeclaration(self.tokens, self.namespace, TokenType.IDENTIFIER, self.gui).parse_statement(
                                current_index)
                        elif current_token.val == 'show':
                            ShowStatement(self.tokens, self.namespace, self.gui).parse_statement(current_index)
                    elif current_token.token_type == TokenType.IDENTIFIER and current_index < len(self.tokens) - 1 and self.tokens[current_index + 1].val == '=':
                        Operation(self.tokens, self.namespace, self.gui).parse_statement(current_index)

                    current_index += 1
                current_index = index
                return current_index
            current_index += 1
        return index

    def false_statement(self,index):
        current_index = index + 1
        while current_index < len(self.tokens):
            if self.tokens[current_index].val == '{':
                brace_count = 1
                current_index += 1
                while current_index < len(self.tokens) and brace_count > 0:
                    if self.tokens[current_index].val == '{':
                        brace_count += 1
                    elif self.tokens[current_index].val == '}':
                        brace_count -= 1
                    current_index += 1

                return current_index-1
            current_index += 1
        return index