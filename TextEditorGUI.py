import tkinter as tk
from tkinter import font,filedialog


class TextEditorGUI:

    def __init__(self):

        self.main_window = tk.Tk()
        self.container_frame = tk.Frame(self.main_window)
        self.text_editor = tk.Text(self.container_frame,wrap=tk.WORD,undo=True)
        self.text_scroll = tk.Scrollbar(self.container_frame,command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.text_scroll.set)
        self.frame = tk.Frame(self.main_window)

        self.current_font = tk.StringVar(self.main_window)
        self.fonts = ["Arial","Helvetica","Times New Roman","Courier New","Gadget","Copperplate Gothic Light"]
        self.font_label = tk.Label(self.frame, text="Font Options")
        self.font_menu = tk.OptionMenu(self.frame, self.current_font, *self.fonts, command=lambda opt: self.change_font(opt))

        self.size_label = tk.Label(self.frame, text="Size Options")
        self.current_font_size = tk.StringVar(self.main_window)
        self.fonts = ["Arial","Helvetica","Times New Roman","Courier New","Gadget","Copperplate Gothic Light"]
        self.sizes = [i for i in range(8,40,2)]
        self.font_size_menu = tk.OptionMenu(self.frame, self.current_font_size, *self.sizes, command=lambda opt: self.change_font_size(opt))

        self.filetype = (('text files', '*.txt'), ('all files', '*.*'))

        self.result_label = tk.Label(self.container_frame, text="Result:")
        self.result_display = tk.Text(self.container_frame, wrap=tk.WORD, width=80, height=5)


        self.current_file = None
        self.create_file_ops()

    def change_font(self, font_opt):
        font_obj = font.Font(family=font_opt,size=int(self.current_font_size.get()))
        if self.text_editor.tag_ranges(tk.SEL):
            self.text_editor.tag_configure("user_font", font=font_obj)
            self.text_editor.tag_add("user_font", "sel.first", "sel.last")
        else:
            self.text_editor.configure(font=font_obj)

    def change_font_size(self, font_size_opt):
        font_obj = font.Font(family=self.current_font.get(),size=int(font_size_opt))
        if self.text_editor.tag_ranges(tk.SEL):
            self.text_editor.tag_configure("user_font", font=font_obj)
            self.text_editor.tag_add("user_font", "sel.first", "sel.last")
        else:
            self.text_editor.configure(font=font_obj)

    def open_file(self):
        try:
            open_file = filedialog.askopenfilename(filetypes=self.filetype)
            with open(open_file,'r') as filee:
                text = filee.read()
                self.text_editor.delete('1.0',tk.END)
                self.text_editor.insert(tk.END,text)
        except FileNotFoundError:
            print('the file does not exist')

    def save_as_file(self):
        try:
            to_save_file = filedialog.asksaveasfilename(filetypes=self.filetype,defaultextension='.txt')
            with open(to_save_file,'w') as filee:
                filee.write(self.text_editor.get('1.0',tk.END))
            self.current_file = to_save_file
        except FileNotFoundError:
            print('the file is not saved')

    def save_file(self):

        if not self.current_file:
            self.save_as_file()
        else:
            with open(self.current_file,'w') as filee:
                filee.write(self.text_editor.get('1.0',tk.END))

    def create_file_ops(self):

        self.open_button = tk.Button(self.frame, text="Open File",command=self.open_file)
        self.save_button = tk.Button(self.frame, text="Save File",command=self.save_file)
        self.save_as_button = tk.Button(self.frame, text="Save as...",command=self.save_as_file)
        self.undo_button = tk.Button(self.frame, text="Undo",command=self.text_editor.edit_undo)
        self.redo_button = tk.Button(self.frame, text="Redo",command=self.text_editor.edit_redo)
        self.run_button = tk.Button(self.frame,text='Execute')

    def organize_components(self):
        self.main_window.title("My Text Editor")
        self.main_window.geometry("800x600")

        self.container_frame.grid(row=0,column=0,sticky="nsew")
        self.text_editor.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.text_scroll.pack(side=tk.RIGHT,fill=tk.Y)

        self.result_label.pack(side=tk.TOP, pady=(10,0))
        self.result_display.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.frame.grid(row=0, column=2, sticky="n")
        self.font_label.grid(row=0, column=0, pady=5)
        self.current_font.set(self.fonts[0])

        self.font_menu.grid(row=1, column=0, pady=5)

        self.size_label.grid(row=2, column=0, pady=5)
        self.current_font_size.set('12')
        self.font_size_menu.grid(row=3, column=0, pady=5)

        self.open_button.grid(row=4, column=0, pady=5)
        self.save_button.grid(row=5, column=0, pady=5)
        self.save_as_button.grid(row=6, column=0, pady=5)
        self.undo_button.grid(row=7, column=0, pady=5)
        self.redo_button.grid(row=8, column=0, pady=5)
        self.run_button.grid(row=9, column=0, pady=5)

        self.main_window.grid_rowconfigure(0,weight=1)
        self.main_window.grid_columnconfigure(0,weight=1)

    def retrieve_code(self):
        return self.text_editor.get('1.0', tk.END)

    def display_result_msg(self,result):
        self.result_display.insert(tk.END, result)

    def clear_display(self):
        self.result_display.delete('1.0', tk.END)

    def run(self):
        self.organize_components()
        self.main_window.mainloop()

# ob = TextEditor()
# ob.run()


