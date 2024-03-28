# **Custom Language Interpreter**

**Introduction**

This project is a Custom Language Interpreter written in Python, designed to interpret a simple custom language. The custom language includes features such as variable declaration **(dec)**, printing values **(show())**, and control flow statements including **if, elif, else, and while**.

**Features**

1. Variable Declaration **(dec)**: Allows users to declare variables in the custom language.
  **dec a**
  The above line simply declares a variable, as it os not initialized yet, its value is None. 
  or 
  **dec a = 5**
  In the above case, a variable is declared and initialized. 

2. Printing Values **(show())**: Acts as the **print()** function in Python, displaying values on the output display.
  **dec a = 5
    show(a)**
   The above line 5 wil be shown inside the display part.
   **Warning**
   Do not try to print expressions like show(1+1), that will result in error 

4. Control Flow Statements: Supports **if, elif, else, and while** statements for conditional and looping constructs.
   All statements should be stated inside the **parenthesis (...)** and the code blocks are defined inside the **curly brackets** **{...}**.
   The code also supports nested statements.
    **dec a
    a = 10
    if (a < 111) {
    a = 88
    show(a)
    }
    elif (a > 20) {
    a = 99
    show(a)
    }**
   or
     **while(a<10){
      a = a + 1
      show(a)
      while(b<5){
          b = b + 1
          show("b is",b)
      }
  }
  show("new",a)**
   or
    **dec a
    a=1
    while(a<10){
        a = a + 1
        if(a>5){
           show(a)
        }
    }
    show(a)**
    

**Usage**

Text Editor Interface: The program provides a Text Editor interface using the Python's Tkinter library. Upon starting the interpreter, the Text Editor opens, allowing users to write code in the custom language. Later the code can be saved using buttons **Save** or **Save as**, an existing file can be opened by using the **Open** button. Also, user can change the font and the size of the text, and do **Undo/Redo** operations.
Writing Code: Users can write their code in the Text Editor, utilizing features such as variable declaration, printing values, and control flow statements.
Executing Code: After writing the code, users can execute it by pressing the **Execute** button.
Output Display: The results of the executed code will be shown in the **output display section** of the interface.
