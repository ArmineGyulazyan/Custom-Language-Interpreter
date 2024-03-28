import TextEditorGUI
import Lexer
import Parser

class Interpreter:

    def __init__(self):

        self.text_editor_gui = TextEditorGUI.TextEditorGUI()
        self.text_editor_gui.run_button.config(command=self.execute_code)

        self.text_editor_gui.run()


        self.lexer = None
        self.parser = None

    def execute_code(self):
        self.text_editor_gui.clear_display()

        char_stream = self.text_editor_gui.retrieve_code()
        self.lexer = Lexer.Lexer(char_stream,self.text_editor_gui)
        tokens = self.lexer.tokenize_text()
        self.parser = Parser.Parser(tokens, self.text_editor_gui)
        self.parser.parse()