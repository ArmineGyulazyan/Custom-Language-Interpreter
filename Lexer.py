from typing import List
import re
import Token

class Lexer:

    def __init__(self,char_stream,gui):

        self.char_stream = char_stream
        self.gui = gui
        self.tokens: List[Token.Token] = []


    def add_token(self,token_type,val):
        self.tokens.append(Token.Token(token_type,val))

    def tokenize_text(self):

        self.tokens = []

        lines = self.char_stream.splitlines()
        #regex-ov custom lezun tokenneri patternneri enq bajanum
        #amen tuple parunakuma konkret tokeni type, vortex arajin elementy token_typei anunna, 2rdy regex patternna
        token_specs = [
            ('KEYWORD', r'\bdec\b|\bshow\b|\bif\b|\belif\b|\belse\b|\bwhile\b'),  #'dec'kam'show' ev ayl Keywordneri hamar, \b-i shnorhiv nayum enq, vor arandzin barer linen nor hamarven keyword, voch te substring
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'), #identifier-nery piti sksen kam mecatarov,kam poqratarov kam underscoreov, *-ov` mnacacy karox en linel nayev tver,karoxe en krknvel,tarber kombinacianeri hamar
            ('PARENTHESIS', r'[(){}]'),
            ('NUMBER', r'\b\d+(\.\d+)?\b'), #integerneri u decimalneri hamara, d-n 0-9 tvern en +ov el asum enq, vor karan mi qani hat tvanshanner linen, (\.\d+)? ays masum asum enq, vor arajin char-ic heto karox e . linel kam chlinel` yst ?-i
            ('STRING', r'"[^"]*"'), #stringeri hamar, piti partadir sksen double quotenerov, asum enq, vor double quote-ov sksum enq, dranic heto cankacac char kara lini baci "-ic
            ('OPERATOR', r'[\+\-\*/%=<>!&|^]=?|\&\&|\|\|'),
            ('COMMA', r','),
            ('SKIP', r'[ \t]+'),  #baca toxnum spaceern u tabery
            ('MISMATCH', r'.')  #any other character, '.'-ov asum enq, vor khamapatasxani, ete verevum nshvac patterneric voch mekin match chi exel
        ]


        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
        print(token_regex)
        #re.finditer-ov tvyal line-i elementnery hamapatasxanacnuma token_regex-i voreve xmbi
        #match_ob-i lastgroup attribute-ov stanum enq verjin match exac token_type-i anuny,orinak` IDENTIFIER
        #match_ob-i group() methodov stanum enq hamapatasxan keyword-y, orinak 'dec'
        for line in lines:
            for match_ob in re.finditer(token_regex,line):
                print('match_ob->',match_ob)
                typee = match_ob.lastgroup
                print('match_ob.lastgroup->',typee)
                value = match_ob.group()
                print('match_ob.group()->',value)
                if typee == 'SKIP':
                    continue
                elif typee == 'MISMATCH':
                    self.gui.display_result_msg(f'SyntaxError: Unexpected character, {value!r} in line <{line}>')
                    return
                else:
                    print(Token.TokenType[typee])
                    self.tokens.append(Token.Token(Token.TokenType[typee],value))

        for i in self.tokens:
            print('<',i.token_type,i.val,'>')
        return self.tokens



