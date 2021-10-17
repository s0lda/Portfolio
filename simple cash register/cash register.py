import tkinter as tk
import os, json
from typing import Any
from tkinter import DoubleVar, PhotoImage, StringVar, ttk
from tkinter.constants import CENTER, NO


class Application(tk.Tk):
    def __init__(self, database: 'StockDatabase', settings: 'TillSettings', payments: 'Payments') -> None:
        super().__init__()
        self._db = database
        self._sett = settings
        self._pay = payments
        
        self.geometry('500x500+100+100')
        self.title('Cash Register')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        
        self.create_buttons()
        self.create_purchase_list()
        self.create_labels()
    

    # function to check if some of StringVars are float for valid input
    # using DoubleVar will throw an error if someone will input a string
    def is_float(self, valueToCheck: str) -> float:
        try:
            return float(valueToCheck)
        except ValueError:
            return 0


    def create_buttons(self) -> None:
        add_to_cart = ttk.Button(self, text='Add to basket', command=self.add_to_basket)
        add_to_cart.place(x=10, y=10, width=90, height=50)

        delete_from_cart = ttk.Button(self, text='Remove', command=self.remove_from_basket)
        delete_from_cart.place(x=10, y=70, width=90, height=50)
        
        stock_managment = ttk.Button(self, text='Manage Stock', command=self.manage_stock_window)
        stock_managment.place(x=10, y=430, width=90)
        
        exit_button = ttk.Button(self, text='EXIT', command= self.destroy)
        exit_button.place(x=10, y=460, width=90)
        
        payment_button = ttk.Button(self, text='PAY', command=self.get_payment)
        payment_button.place(x=390, y=420, height=70, width=90)


    def create_purchase_list(self) -> None:
        columns = ('#1', '#2', '#3', '#4')
        # set shopping list panel
        self.shopping_list = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.shopping_list.place(x=150, y=10, width=330, height=400)

        self.shopping_list.heading('#1', text='Product')
        self.shopping_list.heading('#2', text='#')       # quantity
        self.shopping_list.heading('#3', text='#')       # price per item
        self.shopping_list.heading('#4', text='Sum')

        self.shopping_list.column('#1', anchor=CENTER, stretch=NO, width=157)
        self.shopping_list.column('#2', anchor=CENTER, stretch=NO, width=50)
        self.shopping_list.column('#3', anchor=CENTER, stretch=NO, width=50)
        self.shopping_list.column('#4', anchor=CENTER, stretch=NO, width=70)
        # set scrollbar for shopping list
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.shopping_list.yview)
        self.shopping_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=481, y=10, height=400)


    # add button function for Manage Stock Window
    def add_new_item(self) -> None:
        new_item_win = tk.Toplevel()
        new_item_win.geometry('300x200+200+200')
        new_item_win.title('New Item Menu')
        
        # set labels
        name_label = ttk.Label(new_item_win, text='Product:')
        name_label.place(x=10, y=10)
        price_label = ttk.Label(new_item_win, text='Price:')
        price_label.place(x=10, y=30)
        purchase_label = ttk.Label(new_item_win, text='Purchase Price:')
        purchase_label.place(x=10, y=50)
        quantity_label = ttk.Label(new_item_win, text='Quantity:')
        quantity_label.place(x=10, y=70)

        # set entry points
        self.name_var = StringVar(value='Product')
        name_entry = ttk.Entry(new_item_win, textvariable=self.name_var, justify='right')
        name_entry.place(x=150, y=10)
        
        self.price_var = StringVar(value='0.0')
        price_entry = ttk.Entry(new_item_win, textvariable=self.price_var, justify='right')
        price_entry.place(x=150, y=30)

        self.purchase_var = StringVar(value='0.0')
        purchase_entry = ttk.Entry(new_item_win, textvariable=self.purchase_var, justify='right')
        purchase_entry.place(x=150, y=50)

        self.item_quantity_var = StringVar(value='0.0')
        quantity_entry = ttk.Entry(new_item_win, textvariable=self.item_quantity_var, justify='right')
        quantity_entry.place(x=150, y=70)

        # window buttons
        cancel_button = ttk.Button(new_item_win, text='CANCEL', command=new_item_win.destroy)
        cancel_button.place(x=190, y=150, height=30)
        add_button = ttk.Button(new_item_win, text='ADD ITEM', command=lambda: [StockDatabase.add_new_stock_item(self._db, [self.name_var.get(), 
                                                                                                                    self.is_float(self.price_var.get()), 
                                                                                                                    self.is_float(self.purchase_var.get()), 
                                                                                                                    self.is_float(self.item_quantity_var.get())]), 
                                                                            new_item_win.destroy(), 
                                                                            self.mng_stock_win.destroy(), 
                                                                            self.manage_stock_window()])
        add_button.place(x=30, y=150, height=30)


    def manage_stock_window(self) -> None:
        self.mng_stock_win = tk.Toplevel()
        self.mng_stock_win.geometry('350x600+150+100')
        self.mng_stock_win.title('Stock Manager')


        cancel_button = ttk.Button(self.mng_stock_win, text='CANCEL', command=self.mng_stock_win.destroy)
        cancel_button.place(x=250, y=550, height=30)
        add_button = ttk.Button(self.mng_stock_win, text='ADD', command=self.add_new_item)
        add_button.place(x=10, y=550, height=30)
        
        
        # msw = Manage Stock Window
        msw_columns = ('#1', '#2', '#3', '#4')
        stock_list = ttk.Treeview(self.mng_stock_win, columns=msw_columns, show='headings', height=27, selectmode='browse')
        stock_list.place(x=10, y=10, width=315, height=500)

        stock_list.heading('#1', text='Product')
        stock_list.heading('#2', text='Price')
        stock_list.heading('#3', text='Purchase Price')
        stock_list.heading('#4', text='Quantity')

        stock_list.column('#1', anchor=CENTER, stretch=NO, width=133)
        stock_list.column('#2', anchor=CENTER, stretch=NO, width=60)
        stock_list.column('#3', anchor=CENTER, stretch=NO, width=60)
        stock_list.column('#4', anchor=CENTER, stretch=NO, width=60)

        scrollbar = ttk.Scrollbar(self.mng_stock_win, orient='vertical', command=self.shopping_list.yview)
        stock_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=325, y=10, height=500)


        # insert data to stock list
        for item in StockDatabase.load_data(self._db):
            stock_list.insert('', tk.END, values=item)


        def delete_item() -> None:
            # get choosen item
            current_item = stock_list.focus()
            item_info = stock_list.item(current_item)
            item_details: Any = item_info["values"]
            
            # excepting index error if someone would press delete when stock list is empty
            try:
                # corrected for 'for' loop comparison. .focus() .item() returned all values as str
                corrected_type: Any = (item_details[0], float(item_details[1]), float(item_details[2]), float(item_details[3]))

                # delete item
                new_data: list[Any] = []
                for item in StockDatabase.load_data(self._db):
                    if item != corrected_type:
                        new_data.append(item)
                # database update procedure
                StockDatabase.create_new_stock_file(self._db)

                for item in new_data:
                    StockDatabase.add_new_stock_item(self._db, item)

                # refresh stock list
                self.mng_stock_win.destroy()
                self.manage_stock_window()
            except IndexError:
                pass


        # delete button
        delete_button = ttk.Button(self.mng_stock_win, text='DELETE', command=delete_item)
        delete_button.place(x=170, y=550, height=30)


        def amend_item_details() -> None:
            amend_win = tk.Toplevel()
            amend_win.geometry('250x250+200+200')
            amend_win.title('Change details')

            question_label = ttk.Label(amend_win, text='What would you like to change?')
            question_label.place(x=10, y=10)

            item_options = ('Sale Price', 'Purchase Price', 'Stock Quantity')
            choice = StringVar()
            options = ttk.OptionMenu(amend_win,
                                    choice,
                                    item_options[0],
                                    *item_options)
            options.place(x=10, y=47)
            options.config(width=15)

            item_new_data = ttk.Label(amend_win, text='New Data:')
            item_new_data.place(x=10, y=90)

            new_data_entry = ttk.Entry(amend_win, justify='right')
            new_data_entry.place(x=10, y=130)


            def accept_new_data(detailIndex: int, newDetail: Any) -> None:
                # get choosen item
                current_item = stock_list.focus()
                item_info = stock_list.item(current_item)
                item_details: Any = item_info["values"]
                print(item_details)
                # corrected for 'for' loop comparison. .focus() .item() returned all values as str
                corrected_type = (item_details[0], float(item_details[1]), float(item_details[2]), float(item_details[3]))
                print(corrected_type)
                new_data: list[Any] = []
                for item in StockDatabase.load_data(self._db):
                    if item != corrected_type:
                        print(item)
                        new_data.append(item)
                
                # append changed item
                item_details[detailIndex] = float(newDetail)
                # type adjustment as floats were turned into strings
                item_details: Any = (item_details[0], float(item_details[1]), float(item_details[2]), float(item_details[3]))
                new_data.append(item_details)
                print(item_details)
                print(corrected_type)
                StockDatabase.create_new_stock_file(self._db)
                # write to database
                for item in new_data:
                    StockDatabase.add_new_stock_item(self._db, item)
                
                # destroy window after changing details
                amend_win.destroy()
                # refresh stock list
                self.mng_stock_win.destroy()
                self.manage_stock_window()
                

            ok_button = ttk.Button(amend_win, text='UPDATE', command=lambda: accept_new_data(item_options.index(choice.get()) + 1, new_data_entry.get()))
            ok_button.place(x=60, y=200)

            cancel_button = ttk.Button(amend_win, text='CANCEL', command=amend_win.destroy)
            cancel_button.place(x=150, y=200)


        amend_button = ttk.Button(self.mng_stock_win, text='CHANGE', command=amend_item_details)
        amend_button.place(x=90, y=550, height=30)
    

    def add_to_basket(self) -> None:
        basket_win = tk.Toplevel()
        basket_win.geometry('250x200+150+300')
        basket_win.title('Add Item to Basket')

        item_label = ttk.Label(basket_win, text='Item:')
        item_label.place(x=10, y=10)

        quantity_label = ttk.Label(basket_win, text='Quantity:')
        quantity_label.place(x=10, y=70)

        available_label = ttk.Label(basket_win, text='Available:')
        available_label.place(x=10, y=110)


        # load options from available stock
        def get_options() -> list[str]:
            choice: list[str] = []
            for item in StockDatabase.load_data(self._db):
                choice.append(item[0])
            if len(choice) == 0:
                choice = ['Nothing in stock']
            return choice


        self.choosen_item = StringVar()
        options = ttk.OptionMenu(basket_win,
                                self.choosen_item,
                                get_options()[0],
                                *get_options())
        options.place(x=120, y=10)
        options.config(width=15)


        # get maximum quantity of item from stock database
        def get_max_quantity(item: str) -> float:
            for product in StockDatabase.load_data(self._db):
                if product[0] == item:
                    return float(product[3])
            return 0


        self.quantity_var = DoubleVar(value=get_max_quantity(self.choosen_item.get()))
        quantity_amount_label = ttk.Label(basket_win, textvariable=self.quantity_var, justify='right', background='lightgrey', anchor='e')
        quantity_amount_label.place(x=120, y=110, width=120)

        self.entryVar = StringVar(value='0')
        quantity_entry = ttk.Entry(basket_win, textvariable=self.entryVar, justify='right')
        quantity_entry.place(x=120, y=70, width=120)

        cancel_button = ttk.Button(basket_win, text='CANCEL', command=basket_win.destroy)
        cancel_button.place(x=140, y=150)


        # insert maximum available stock in quantity_amount_label, update everytime different option from option menu is choosen
        # x, y, z just to pass argument to callback function, as required by tkinter. otherwise= error
        def update_quantity(x: Any, y: Any, z: Any) -> None:
            self.quantity_var = DoubleVar(value=get_max_quantity(self.choosen_item.get()))
            quantity_amount_label['textvariable'] = self.quantity_var


        self.choosen_item.trace_add('write', update_quantity)


        # create item for the shopping list, calculate sum for product (quantity * price)
        def add_to_shopping_list(item: str, quantity: float) -> None:
            product_to_add: list[Any] = []
            product_to_add.append(item)
            # excepting IndexError if someone will try to add items when stock_data is empty
            # ensure it can't be added more than in the stock
            try:
                if len(self.shopping_list.get_children()) != 0:
                    items_in_basket: list[str] = []
                    for child in self.shopping_list.get_children():
                        items_in_basket.append(self.shopping_list.item(child, 'values')[0])
                        if self.shopping_list.item(child, 'values')[0] == item:
                            quantity_sum = float(self.shopping_list.item(child, 'values')[1]) + quantity
                            if quantity_sum >= get_max_quantity(self.choosen_item.get()):
                                product_to_add.append(get_max_quantity(self.choosen_item.get()))
                            else:
                                product_to_add.append(quantity_sum)
                            self.shopping_list.delete(child)
                        # # adding new element to shopping list if there is product(s) in it already
                    if item not in items_in_basket:
                        if quantity >= get_max_quantity(self.choosen_item.get()):
                            product_to_add.append(get_max_quantity(self.choosen_item.get()))
                        else:
                            product_to_add.append(quantity)
                # adding new product to empty shopping list
                else:
                    if quantity >= get_max_quantity(self.choosen_item.get()):
                        product_to_add.append(get_max_quantity(self.choosen_item.get()))
                    else:
                        product_to_add.append(quantity)
                
                # get price of an item from database
                for product in StockDatabase.load_data(self._db):
                    if product[0] == item:
                        product_to_add.append(product[1])
                # sum price
                total = product_to_add[1] * product_to_add[2]
                product_to_add.append(total)

                self.shopping_list.insert('', tk.END, values=product_to_add)
            except IndexError:
                pass


        add_button = ttk.Button(basket_win, text='ADD', command=lambda: add_to_shopping_list(self.choosen_item.get(), self.is_float(self.entryVar.get())))
        add_button.place(x=30, y=150)


    def create_labels(self) -> None:
        total_label = ttk.Label(self, text='TOTAL:')
        total_label.place(x=150, y=420)

        tax_label = ttk.Label(self, text='TAX:')
        tax_label.place(x=150, y=445)

        to_pay_label = ttk.Label(self, text='TOTAL TO PAY:')
        to_pay_label.place(x=150, y=470)


        def calculate_total() -> float:
            total: float = 0.0
            for child in self.shopping_list.get_children():
                total += float(self.shopping_list.item(child, 'values')[3])
            return total


        def get_tax_value() -> float:
            for item in TillSettings.load_settings(self._sett):
                for key, value in item.items():
                    if key == 'sales tax':
                        return value
            return 0.0

        # just a basic tax calculation for training purposes
        def calculate_tax(amount: float) -> float:
            return round((amount / 100) * get_tax_value(), 2)


        self.total_var = DoubleVar(value=calculate_total())
        total_value = ttk.Label(self, textvariable=self.total_var, background='lightgrey', width=10, anchor='e')
        total_value.place(x=315, y=420, width=40)

        self.tax_var = DoubleVar(value=calculate_tax(self.total_var.get()))
        tax_value = ttk.Label(self, textvariable=self.tax_var, background='lightgrey', width=10, anchor='e')
        tax_value.place(x=315, y=445)

        self.to_pay_var = DoubleVar(value=self.tax_var.get() + self.total_var.get())
        to_pay_value = ttk.Label(self, textvariable=self.to_pay_var, background='lightgrey', width=10, anchor='e')
        to_pay_value.place(x=315, y=470)


        def update_totals() -> None:
            self.total_var = DoubleVar(value=calculate_total())
            self.tax_var = DoubleVar(value=calculate_tax(self.total_var.get()))
            self.to_pay_var = DoubleVar(value=self.tax_var.get() + self.total_var.get())
            total_value = ttk.Label(self, textvariable=self.total_var, background='lightgrey', width=10, anchor='e')
            total_value.place(x=315, y=420)
            tax_value = ttk.Label(self, textvariable=self.tax_var, background='lightgrey', width=10, anchor='e')
            tax_value.place(x=315, y=445)
            to_pay_value = ttk.Label(self, textvariable=self.to_pay_var, background='lightgrey', width=10, anchor='e')
            to_pay_value.place(x=315, y=470)
            self.after(1000, update_totals)
        update_totals()


    def get_payment(self) -> None:
        # update total payment
        Payments.update_total_payments(self._pay, self.to_pay_var.get())

        # update stock values
        new_data: list[Any] = []
        updated_data: list[Any] = []
        for item in StockDatabase.load_data(self._db):
            item = list(item)
            for child in self.shopping_list.get_children():
                if self.shopping_list.item(child, 'values')[0] == item[0]:
                    item[3] -= float(self.shopping_list.item(child, 'values')[1])
                    updated_data.append(list(item))                  
        
        # get names of bought products
        compare_list: list[str] = []
        for item in updated_data:
            compare_list.append(item[0])
        print(compare_list)
        print(updated_data)
        # append new data with not bought products
        for item in StockDatabase.load_data(self._db):
            if item[0] not in compare_list:
                new_data.append(list(item))
        # append new data with bought products with new values
        for item in updated_data:
            new_data.append(item)
        print(new_data)
        # write to file procedure
        StockDatabase.create_new_stock_file(self._db)

        for item in new_data:
            StockDatabase.add_new_stock_item(self._db, item)

        # clear shopping list after successful purchase
        self.shopping_list.delete(*self.shopping_list.get_children())
        

    def remove_from_basket(self) -> None:
        # except IndexError for deleting when list is empty
        try:
            selected_item = self.shopping_list.selection()[0]
            self.shopping_list.delete(selected_item)
        except IndexError:
            pass


class StockDatabase:
    def __init__(self, dataFile: str) -> None:
        self._stock_file = dataFile

        # check for stock data file existence
        if os.path.isfile(self._stock_file) == True and os.stat(self._stock_file).st_size != 0:
            pass
        else:
            self.create_new_stock_file()


    def create_new_stock_file(self) -> None:
        with open(self._stock_file, 'w') as f:
            write_data: dict[str, list[Any]] = {"stock": []}
            json.dump(write_data, f, indent=4)

    
    def add_new_stock_item(self, newItem: list[Any]):
        item = {
                "item": newItem[0],
                "sale price": newItem[1],
                "purchase price": newItem[2],
                "stock quantity": newItem[3]
        }
        with open(self._stock_file, 'r') as f:
            data = json.load(f)
            data["stock"].append(item)
        with open(self._stock_file, 'w') as f:
            json.dump(data, f, indent=4)


    def load_data(self) -> list[Any]:
        stock_item: list[Any] = []
        with open(self._stock_file, 'r') as f:
            data = json.load(f)
            for item_data in data["stock"]:
                item: str =  item_data["item"]
                sale_price: float = item_data["sale price"]
                purchase_price: float = item_data["purchase price"]
                stock_quantity: float = item_data["stock quantity"]

                stock_item.append((item, sale_price, purchase_price, stock_quantity))
        return stock_item



class TillSettings:
    def __init__(self, dataFile: str) -> None:
        self._sett_file = dataFile

        # check for settings file existence
        if os.path.isfile(self._sett_file) == True and os.stat(self._sett_file).st_size != 0:
            pass
        else:
            self.create_new_sett_file()


    def create_new_sett_file(self) -> None:
        with open(self._sett_file, 'w') as f:
            write_data = {"settings" : [{
                            "sales tax": 0
                            }]
                        }
            json.dump(write_data, f, indent=4)

    
    def load_settings(self) -> list[Any]:
        settings: list[Any] = []
        with open(self._sett_file, 'r') as f:
            data = json.load(f)
            for item in data["settings"]:
                settings.append(item)
        return settings



class Payments:
    def __init__(self, paymentFile: str) -> None:
        self._payment_file = paymentFile

        # check for file existence
        if os.path.isfile(self._payment_file) == True and os.stat(self._payment_file).st_size != 0:
            pass
        else:
            self.create_new_pay_file()

        
    def create_new_pay_file(self) -> None:
        with open(self._payment_file, 'w') as f:
            write_data = {"Total Payments": 0}
            json.dump(write_data, f, indent=4)

    
    def update_total_payments(self, payment: float):
        with open(self._payment_file, 'r') as f:
            data = json.load(f)
            data["Total Payments"] += payment
        with open(self._payment_file, 'w') as f:
            json.dump(data, f, indent=4)



if __name__ == '__main__':
    _stock_file = f'{os.path.dirname(__file__)}\\stock_data.json'
    _sett_file = f'{os.path.dirname(__file__)}\\settings.json'
    _payment_file = f'{os.path.dirname(__file__)}\\payments.json'
    db = StockDatabase(_stock_file)
    sett = TillSettings(_sett_file)
    pay = Payments(_payment_file)
    Application(database=db, settings=sett, payments=pay).mainloop()
