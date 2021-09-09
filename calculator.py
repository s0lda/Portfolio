from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Calculator')

# user_entry = Entry(root, width= 20, borderwidth= 3, bg= 'lightblue', fg= 'black', font= 'Arial 24 bold')
# user_entry.grid(row= 0, column= 0, columnspan= 4, padx= 10, pady= 10)
user_entry = ttk.Entry(root, width= 28, font= 'Arial 18 bold')
user_entry.grid(row= 0, column= 0, columnspan= 4, ipadx= 5, ipady= 5, pady= 10)


def button_click(number):
    current = user_entry.get()
    user_entry.delete(0, END)
    user_entry.insert(0, str(current) + str(number))


def button_clear():
    user_entry.delete(0, END)


def button_equal():
    second_num = user_entry.get()
    user_entry.delete(0, END)
    if math == '+':
        x = f_number + float(second_num)
    elif math == '-':
        x = f_number - float(second_num)
    elif math == '/':
        try:
            x = f_number / float(second_num)
        except ZeroDivisionError:
            x = 0.0
    elif math == '*':
        x = f_number * float(second_num)
    # return int when int and float when float
    if x.is_integer():
        user_entry.insert(0, int(x))
    else:
        user_entry.insert(0, x)


def first_number(procedure):
    first_num = user_entry.get()
    global f_number
    global math
    math = procedure
    f_number = float(first_num)
    user_entry.delete(0, END)

# add dot to operate with floats
def button_add_dot(dot):
    current = user_entry.get()
    user_entry.delete(0, END)
    user_entry.insert(0, str(current) + dot)


# button_0 = Button(root, text= '0', padx= 30, pady= 15, command= lambda: button_click(0), font= 'Arial 18 bold', borderwidth= 3)
# button_1 = Button(root, text= '1', padx= 30, pady= 15, command= lambda: button_click(1), font= 'Arial 18 bold', borderwidth= 3)
# button_2 = Button(root, text= '2', padx= 30, pady= 15, command= lambda: button_click(2), font= 'Arial 18 bold', borderwidth= 3)
# button_3 = Button(root, text= '3', padx= 30, pady= 15, command= lambda: button_click(3), font= 'Arial 18 bold', borderwidth= 3)
# button_4 = Button(root, text= '4', padx= 30, pady= 15, command= lambda: button_click(4), font= 'Arial 18 bold', borderwidth= 3)
# button_5 = Button(root, text= '5', padx= 30, pady= 15, command= lambda: button_click(5), font= 'Arial 18 bold', borderwidth= 3)
# button_6 = Button(root, text= '6', padx= 30, pady= 15, command= lambda: button_click(6), font= 'Arial 18 bold', borderwidth= 3)
# button_7 = Button(root, text= '7', padx= 30, pady= 15, command= lambda: button_click(7), font= 'Arial 18 bold', borderwidth= 3)
# button_8 = Button(root, text= '8', padx= 30, pady= 15, command= lambda: button_click(8), font= 'Arial 18 bold', borderwidth= 3)
# button_9 = Button(root, text= '9', padx= 30, pady= 15, command= lambda: button_click(9), font= 'Arial 18 bold', borderwidth= 3)

# button_plus = Button(root, text= '+', padx= 30, pady= 15, command= lambda: first_number('+'), font= 'Arial 18 bold', borderwidth= 3)
# button_minus = Button(root, text= '-', padx= 32, pady= 15, command= lambda: first_number('-'), font= 'Arial 18 bold', borderwidth= 3)
# button_divide = Button(root, text= '/', padx= 32, pady= 15, command= lambda: first_number('/'), font= 'Arial 18 bold', borderwidth= 3)
# button_multiply = Button(root, text= 'x', padx= 30, pady= 15, command= lambda: first_number('*'), font= 'Arial 18 bold', borderwidth= 3)
# button_equal = Button(root, text= '=', padx= 30, pady= 55, command= button_equal, bg= 'lightblue', font= 'Arial 18 bold', borderwidth= 3)
# button_dot = Button(root, text= '. ', padx= 30, pady= 15, command= lambda: button_add_dot('.'), font= 'Arial 18 bold', borderwidth= 3)
# button_clear = Button(root, text= 'C', padx= 28, pady= 15, command= button_clear, font= 'Arial 18 bold', borderwidth= 3)

button_0 = ttk.Button(root, text= '0', command= lambda: button_click(1))
button_1 = ttk.Button(root, text= '1', command= lambda: button_click(1))
button_2 = ttk.Button(root, text= '2', command= lambda: button_click(2))
button_3 = ttk.Button(root, text= '3', command= lambda: button_click(3))
button_4 = ttk.Button(root, text= '4', command= lambda: button_click(4))
button_5 = ttk.Button(root, text= '5', command= lambda: button_click(5))
button_6 = ttk.Button(root, text= '6', command= lambda: button_click(6))
button_7 = ttk.Button(root, text= '7', command= lambda: button_click(7))
button_0 = ttk.Button(root, text= '0', command= lambda: button_click(0))
button_8 = ttk.Button(root, text= '8', command= lambda: button_click(8))
button_9 = ttk.Button(root, text= '9', command= lambda: button_click(9))

button_plus = ttk.Button(root, text= '+', command= lambda: first_number('+'))
button_minus = ttk.Button(root, text= '-', command= lambda: first_number('-'))
button_divide = ttk.Button(root, text= '/', command= lambda: first_number('/'))
button_multiply = ttk.Button(root, text= 'x', command= lambda: first_number('*'))
button_equal = ttk.Button(root, text= '=', command= button_equal)
button_dot = ttk.Button(root, text= '. ', command= lambda: button_add_dot('.'))
button_clear = ttk.Button(root, text= 'C', command= button_clear)

button_0.grid(row= 5, column= 1, ipadx= 10, ipady= 10)
button_1.grid(row= 4, column= 0, ipadx= 10, ipady= 10)
button_2.grid(row= 4, column= 1, ipadx= 10, ipady= 10)
button_3.grid(row= 4, column= 2, ipadx= 10, ipady= 10)
button_4.grid(row= 3, column= 0, ipadx= 10, ipady= 10)
button_5.grid(row= 3, column= 1, ipadx= 10, ipady= 10)
button_6.grid(row= 3, column= 2, ipadx= 10, ipady= 10)
button_7.grid(row= 2, column= 0, ipadx= 10, ipady= 10)
button_8.grid(row= 2, column= 1, ipadx= 10, ipady= 10)
button_9.grid(row= 2, column= 2, ipadx= 10, ipady= 10)
button_plus.grid(row= 2, column= 3, ipadx= 10, ipady= 10)
button_minus.grid(row= 3, column= 3, ipadx= 10, ipady= 10)
button_divide.grid(row= 1, column= 1, ipadx= 10, ipady= 10)
button_multiply.grid(row= 1, column= 2, ipadx= 10, ipady= 10)
button_equal.grid(row= 4, rowspan= 2,  column= 3, ipadx= 10, ipady= 32)
button_dot.grid(row= 5, column= 2, ipadx= 10, ipady= 10)
button_clear.grid(row= 1, column= 3, ipadx= 10, ipady= 10)

if __name__ == '__main__':
    root.mainloop()

