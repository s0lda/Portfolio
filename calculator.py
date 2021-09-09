from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Calculator')

user_entry = ttk.Entry(root, width= 23, font= 'Arial 18 bold')
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

button_0.grid(row= 5, column= 1, ipadx= 3, ipady= 10)
button_1.grid(row= 4, column= 0, ipadx= 3, ipady= 10)
button_2.grid(row= 4, column= 1, ipadx= 3, ipady= 10)
button_3.grid(row= 4, column= 2, ipadx= 3, ipady= 10)
button_4.grid(row= 3, column= 0, ipadx= 3, ipady= 10)
button_5.grid(row= 3, column= 1, ipadx= 3, ipady= 10)
button_6.grid(row= 3, column= 2, ipadx= 3, ipady= 10)
button_7.grid(row= 2, column= 0, ipadx= 3, ipady= 10)
button_8.grid(row= 2, column= 1, ipadx= 3, ipady= 10)
button_9.grid(row= 2, column= 2, ipadx= 3, ipady= 10)
button_plus.grid(row= 2, column= 3, ipadx= 3, ipady= 10)
button_minus.grid(row= 3, column= 3, ipadx= 3, ipady= 10)
button_divide.grid(row= 1, column= 1, ipadx= 3, ipady= 10)
button_multiply.grid(row= 1, column= 2, ipadx= 3, ipady= 10)
button_equal.grid(row= 4, rowspan= 2,  column= 3, ipadx= 3, ipady= 32)
button_dot.grid(row= 5, column= 2, ipadx= 3, ipady= 10)
button_clear.grid(row= 1, column= 3, ipadx= 3, ipady= 10)


if __name__ == '__main__':
    root.mainloop()
