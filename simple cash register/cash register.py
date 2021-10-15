import tkinter as tk
import os, json
from typing import Any
from tkinter import DoubleVar, StringVar, ttk
from tkinter.constants import CENTER, NO


class Application(tk.Tk):
    def __init__(self, database: 'StockDatabase', settings: 'TillSettings', payments: 'Payments') -> None:
        super().__init__()
        self._db = database
        self._sett = settings
        self._pay = payments
        
        self.geometry('500x500')
        self.geometry('+100+100')
        self.title('Cash Register')
        self.iconbitmap('icon.ico')
        
        self.createButtons()
        self.createPurchaseList()
        self.createLabels()


    def createButtons(self) -> None:
        addToCart = ttk.Button(self, text='Add to basket', command=self.addToBasket)
        addToCart.place(x=10, y=10, width=90, height=50)

        deleteFromCart = ttk.Button(self, text='Remove', command=self.removeFromBasket)
        deleteFromCart.place(x=10, y=70, width=90, height=50)
        
        stockManagment = ttk.Button(self, text='Manage Stock', command=self.manageStockWindow)
        stockManagment.place(x=10, y=430, width=90)
        
        exitButton = ttk.Button(self, text='EXIT', command= self.destroy)
        exitButton.place(x=10, y=460, width=90)
        
        paymentButton = ttk.Button(self, text='PAY', command=self.getPayment)
        paymentButton.place(x=390, y=420, height=70, width=90)


    def createPurchaseList(self) -> None:
        columns = ('#1', '#2', '#3', '#4')
        # set shopping list panel
        self.shoppingList = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.shoppingList.place(x=150, y=10, width=330, height=400)

        self.shoppingList.heading('#1', text='Product')
        self.shoppingList.heading('#2', text='#')       # quantity
        self.shoppingList.heading('#3', text='#')       # price per item
        self.shoppingList.heading('#4', text='Sum')

        self.shoppingList.column('#1', anchor=CENTER, stretch=NO, width=157)
        self.shoppingList.column('#2', anchor=CENTER, stretch=NO, width=50)
        self.shoppingList.column('#3', anchor=CENTER, stretch=NO, width=50)
        self.shoppingList.column('#4', anchor=CENTER, stretch=NO, width=70)
        # set scrollbar for shopping list
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.shoppingList.yview)
        self.shoppingList.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=481, y=10, height=400)


    def manageStockWindow(self) -> None:
        mngStockWin = tk.Toplevel()
        mngStockWin.geometry('350x600')
        mngStockWin.geometry('+150+100')
        mngStockWin.title('Stock Manager')
        mngStockWin.iconbitmap('icon.ico')

        def addNewItem() -> None:
            newItemWin = tk.Toplevel()
            newItemWin.geometry('300x200')
            newItemWin.geometry('+200+200')
            newItemWin.title('New Item Menu')
            newItemWin.iconbitmap('icon.ico')
            
            # set labels
            nameLabel = ttk.Label(newItemWin, text='Product:')
            nameLabel.place(x=10, y=10)
            priceLabel = ttk.Label(newItemWin, text='Price:')
            priceLabel.place(x=10, y=30)
            purchaseLabel = ttk.Label(newItemWin, text='Purchase Price:')
            purchaseLabel.place(x=10, y=50)
            quantityLabel = ttk.Label(newItemWin, text='Quantity:')
            quantityLabel.place(x=10, y=70)

            # set entry points
            tk.nameVar = StringVar(value='Product')
            nameEntry = ttk.Entry(newItemWin, textvariable=tk.nameVar, justify='right')
            nameEntry.place(x=150, y=10)
            
            tk.priceVar = DoubleVar(value=0.0)
            priceEntry = ttk.Entry(newItemWin, textvariable=tk.priceVar, justify='right')
            priceEntry.place(x=150, y=30)

            tk.purchaseVar = DoubleVar(value=0.0)
            purchaseEntry = ttk.Entry(newItemWin, textvariable=tk.purchaseVar, justify='right')
            purchaseEntry.place(x=150, y=50)

            tk.quantityVar = DoubleVar(value=0.0)
            quantityEntry = ttk.Entry(newItemWin, textvariable=tk.quantityVar, justify='right')
            quantityEntry.place(x=150, y=70)


            # window buttons
            cancelButton = ttk.Button(newItemWin, text='CANCEL', command=newItemWin.destroy)
            cancelButton.place(x=190, y=150, height=30)
            addButton = ttk.Button(newItemWin, text='ADD ITEM', command=lambda: [StockDatabase.addNewStockItem(self._db, [tk.nameVar.get(), 
                                                                                                                        tk.priceVar.get(), 
                                                                                                                        tk.purchaseVar.get(), 
                                                                                                                        tk.quantityVar.get()]), 
                                                                                newItemWin.destroy(), 
                                                                                mngStockWin.destroy(), 
                                                                                self.manageStockWindow()])
            addButton.place(x=30, y=150, height=30)
            

        cancelButton = ttk.Button(mngStockWin, text='CANCEL', command=mngStockWin.destroy)
        cancelButton.place(x=250, y=550, height=30)
        addButton = ttk.Button(mngStockWin, text='ADD', command=addNewItem)
        addButton.place(x=10, y=550, height=30)
        
        
        # msw = Manage Stock Window
        mswColumns = ('#1', '#2', '#3', '#4')
        stockList = ttk.Treeview(mngStockWin, columns=mswColumns, show='headings', height=27, selectmode='browse')
        stockList.place(x=10, y=10, width=315, height=500)

        stockList.heading('#1', text='Product')
        stockList.heading('#2', text='Price')
        stockList.heading('#3', text='Purchase Price')
        stockList.heading('#4', text='Quantity')

        stockList.column('#1', anchor=CENTER, stretch=NO, width=133)
        stockList.column('#2', anchor=CENTER, stretch=NO, width=60)
        stockList.column('#3', anchor=CENTER, stretch=NO, width=60)
        stockList.column('#4', anchor=CENTER, stretch=NO, width=60)

        scrollbar = ttk.Scrollbar(mngStockWin, orient=tk.VERTICAL, command=self.shoppingList.yview)
        stockList.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=325, y=10, height=500)

        # insert data to stock list
        for item in StockDatabase.loadData(self._db):
            stockList.insert('', tk.END, values=item)


        def deleteItem() -> None:
            # get choosen item
            currentItem = stockList.focus()
            itemInfo = stockList.item(currentItem)
            itemDetails = itemInfo["values"]
            
            # excepting index error if someone would press delete when stock list is empty
            try:
                # corrected for 'for' loop comparison. .focus() .item() returned all values as str
                correctedType = (itemDetails[0], float(itemDetails[1]), float(itemDetails[2]), float(itemDetails[3]))

                # delete item
                newData: list[Any] = []
                for item in StockDatabase.loadData(self._db):
                    if item != correctedType:
                        newData.append(item)

                StockDatabase.createNewStockFile(self._db)

                for item in newData:
                    StockDatabase.addNewStockItem(self._db, item)

                # refresh stock list
                mngStockWin.destroy()
                self.manageStockWindow()
            except IndexError:
                pass


        # delete button
        deleteButton = ttk.Button(mngStockWin, text='DELETE', command=deleteItem)
        deleteButton.place(x=170, y=550, height=30)


        def amendItemDetails() -> None:
            amendWin = tk.Toplevel()
            amendWin.geometry('250x250')
            amendWin.geometry('+200+200')
            amendWin.title('Change details')
            amendWin.iconbitmap('icon.ico')

            questionLabel = ttk.Label(amendWin, text='What would you like to change?')
            questionLabel.place(x=10, y=10)

            itemOptions = ('Sale Price', 'Purchase Price', 'Stock Quantity')
            choice = StringVar()
            options = ttk.OptionMenu(amendWin,
                                    choice,
                                    itemOptions[0],
                                    *itemOptions)
            options.place(x=10, y=47)
            options.config(width=15)

            itemNewData = ttk.Label(amendWin, text='New Data:')
            itemNewData.place(x=10, y=90)

            newDataEntry = ttk.Entry(amendWin, justify='right')
            newDataEntry.place(x=10, y= 130)


            def acceptNewData(detailIndex: int, newDetail: Any) -> None:
                # get choosen item
                currentItem = stockList.focus()
                itemInfo = stockList.item(currentItem)
                itemDetails = itemInfo["values"]
                print(itemDetails)
                # corrected for 'for' loop comparison. .focus() .item() returned all values as str
                correctedType = (itemDetails[0], float(itemDetails[1]), float(itemDetails[2]), float(itemDetails[3]))
                print(correctedType)
                newData: list[Any] = []
                for item in StockDatabase.loadData(self._db):
                    if item != correctedType:
                        print(item)
                        newData.append(item)
                
                # append changed item
                itemDetails[detailIndex] = float(newDetail)
                # type adjustment as floats were turned into strings
                itemDetails = (itemDetails[0], float(itemDetails[1]), float(itemDetails[2]), float(itemDetails[3]))
                newData.append(itemDetails)
                print(itemDetails)
                print(correctedType)
                StockDatabase.createNewStockFile(self._db)
                # write to database
                for item in newData:
                    StockDatabase.addNewStockItem(self._db, item)
                
                # destroy window after changing details
                amendWin.destroy()
                # refresh stock list
                mngStockWin.destroy()
                self.manageStockWindow()
                

            okButton = ttk.Button(amendWin, text='UPDATE', command=lambda: acceptNewData(itemOptions.index(choice.get()) + 1, newDataEntry.get()))
            okButton.place(x=60, y=200)

            cancelButton = ttk.Button(amendWin, text='CANCEL', command=amendWin.destroy)
            cancelButton.place(x=150, y=200)


        amendButton = ttk.Button(mngStockWin, text='CHANGE', command=amendItemDetails)
        amendButton.place(x=90, y=550, height=30)
    

    def addToBasket(self) -> None:
        basketWin = tk.Toplevel()
        basketWin.geometry('250x200')
        basketWin.geometry('+200+200')
        basketWin.title('Add Item to Basket')
        basketWin.iconbitmap('icon.ico')

        itemLabel = ttk.Label(basketWin, text='Item:')
        itemLabel.place(x=10, y=10)

        quantityLabel = ttk.Label(basketWin, text='Quantity:')
        quantityLabel.place(x=10, y=70)

        availableLAbel = ttk.Label(basketWin, text='Available:')
        availableLAbel.place(x=10, y=110)


        # load options from available stock
        def getOptions() -> list[str]:
            choice: list[str] = []
            for item in StockDatabase.loadData(self._db):
                choice.append(item[0])
            if len(choice) == 0:
                choice = ['Nothing in stock']
            return choice


        tk.choosenItem = StringVar()
        options = ttk.OptionMenu(basketWin,
                                tk.choosenItem,
                                getOptions()[0],
                                *getOptions())
        options.place(x=120, y=10)
        options.config(width=15)


        # get maximum quantity of item from stock database
        def getMaxQuantity(item: str) -> float:
            for product in StockDatabase.loadData(self._db):
                if product[0] == item:
                    return float(product[3])


        tk.quantityVar = DoubleVar(value=getMaxQuantity(tk.choosenItem.get()))
        quantityAmountLabel = ttk.Label(basketWin, textvariable=tk.quantityVar, justify='right', background='lightgrey', anchor='e')
        quantityAmountLabel.place(x=120, y=110, width=120)

        tk.entryVar = DoubleVar()
        quantityEntry = ttk.Entry(basketWin, textvariable=tk.entryVar, justify='right')
        quantityEntry.place(x=120, y=70, width=120)

        cancelButton = ttk.Button(basketWin, text='CANCEL', command=basketWin.destroy)
        cancelButton.place(x=140, y=150)


        # insert maximum available stock in Entry, update everytime different option from option menu is choosen
        # x, y, z just to pass argument to callback function, as required by tkinter. otherwise= error
        def updateQuantity(x: Any, y: Any, z: Any) -> None:
            tk.quantityVar = DoubleVar(value=getMaxQuantity(tk.choosenItem.get()))
            quantityAmountLabel['textvariable'] = tk.quantityVar


        tk.choosenItem.trace_add('write', updateQuantity)

        '''NEED TO WORK ON THIS PART
        EVERYTHING IS WORKING FINE, BUT WHILE ADDING SAME ITEM MULTIPLE TIMES
        WHEN IT COMES TO PAYMENT TIME stock_data.json IS NOT UPDATED CORRECTLY.
        NEED TO FIND THE WAY TO CONSOLIDATE ITEMS IN THE shoppingList'''
        # create item for the shopping list, calculate sum for product (quantity * price)
        def addToShoppingList(item: str, quantity: float) -> None:
            productToAdd: list[Any] = []
            productToAdd.append(item)
            # excepting TypeError if someone will try to add items when stock_data is empty
            try:
                # ensure it can't be added more than in the stock
                if quantity >= getMaxQuantity(tk.choosenItem.get()):
                    productToAdd.append(getMaxQuantity(tk.choosenItem.get()))
                else:
                    productToAdd.append(quantity)
                for product in StockDatabase.loadData(self._db):
                    if product[0] == item:
                        productToAdd.append(product[1])
                total = productToAdd[1] * productToAdd[2]
                productToAdd.append(total)

                self.shoppingList.insert('', tk.END, values=productToAdd)
            except TypeError:
                pass


        addButton = ttk.Button(basketWin, text='ADD', command=lambda: addToShoppingList(tk.choosenItem.get(), tk.entryVar.get()))
        addButton.place(x=30, y=150)


    def createLabels(self) -> None:
        totalLabel = ttk.Label(self, text='TOTAL:')
        totalLabel.place(x=150, y=420)

        taxLabel = ttk.Label(self, text='TAX:')
        taxLabel.place(x=150, y=445)

        toPayLabel = ttk.Label(self, text='TOTAL TO PAY:')
        toPayLabel.place(x=150, y=470)


        def calculateTotal() -> float:
            total: float = 0.0
            for child in self.shoppingList.get_children():
                total += float(self.shoppingList.item(child, 'values')[3])
            return total


        def getTaxValue() -> float:
            for item in TillSettings.loadSettings(self._sett):
                for key, value in item.items():
                    if key == 'sales tax':
                        return value
            return 0.0

        # just a basic tax calculation for training purposes
        def calculateTax(amount: float) -> float:
            return round((amount / 100) * getTaxValue(), 2)


        self.totalVar = DoubleVar(value=calculateTotal())
        totalValue = ttk.Label(self, textvariable=self.totalVar, background='lightgrey', width=10, anchor='e')
        totalValue.place(x=315, y=420, width=40)

        self.taxVar = DoubleVar(value=calculateTax(self.totalVar.get()))
        taxValue = ttk.Label(self, textvariable=self.taxVar, background='lightgrey', width=10, anchor='e')
        taxValue.place(x=315, y=445)

        self.toPayVar = DoubleVar(value=self.taxVar.get() + self.totalVar.get())
        toPayValue = ttk.Label(self, textvariable=self.toPayVar, background='lightgrey', width=10, anchor='e')
        toPayValue.place(x=315, y=470)


        def updateTotals() -> None:
            self.totalVar = DoubleVar(value=calculateTotal())
            self.taxVar = DoubleVar(value=calculateTax(self.totalVar.get()))
            self.toPayVar = DoubleVar(value=self.taxVar.get() + self.totalVar.get())
            totalValue = ttk.Label(self, textvariable=self.totalVar, background='lightgrey', width=10, anchor='e')
            totalValue.place(x=315, y=420)
            taxValue = ttk.Label(self, textvariable=self.taxVar, background='lightgrey', width=10, anchor='e')
            taxValue.place(x=315, y=445)
            toPayValue = ttk.Label(self, textvariable=self.toPayVar, background='lightgrey', width=10, anchor='e')
            toPayValue.place(x=315, y=470)
            self.after(1000, updateTotals)
        updateTotals()


    def getPayment(self) -> None:
        # update total payment
        Payments.updateTotalPayments(self._pay, self.toPayVar.get())

        # update stock values
        newData: list[Any] = []
        updatedData: list[Any] = []
        for item in StockDatabase.loadData(self._db):
            item = list(item)
            for child in self.shoppingList.get_children():
                if self.shoppingList.item(child, 'values')[0] == item[0]:
                    item[3] -= float(self.shoppingList.item(child, 'values')[1])
                    updatedData.append(list(item))                  
        
        # get names of bought products
        compareList: list[str] = []
        for item in updatedData:
            compareList.append(item[0])
        print(compareList)
        print(updatedData)
        # append new data with not bought products
        for item in StockDatabase.loadData(self._db):
            if item[0] not in compareList:
                newData.append(list(item))
        # append new data with bought products with new values
        for item in updatedData:
            newData.append(item)
        print(newData)
        # write to file procedure
        StockDatabase.createNewStockFile(self._db)

        for item in newData:
            StockDatabase.addNewStockItem(self._db, item)

        # clear shopping list after successful purchase
        self.shoppingList.delete(*self.shoppingList.get_children())
        

    def removeFromBasket(self) -> None:
        # except IndexError for deleting when list is empty
        try:
            selectedItem = self.shoppingList.selection()[0]
            self.shoppingList.delete(selectedItem)
        except IndexError:
            pass


class StockDatabase:
    def __init__(self, dataFile: str) -> None:
        self._stockFile = dataFile

        # check for stock data file existence
        if os.path.isfile(self._stockFile) == True and os.stat(self._stockFile).st_size != 0:
            pass
        else:
            self.createNewStockFile()


    def createNewStockFile(self) -> None:
        with open(self._stockFile, 'w') as f:
            writeData: dict[str, list[Any]] = {"stock": []}
            json.dump(writeData, f, indent=4)

    
    def addNewStockItem(self, newItem: list[Any]):
        item = {
                "item": newItem[0],
                "sale price": newItem[1],
                "purchase price": newItem[2],
                "stock quantity": newItem[3]
        }
        with open(self._stockFile, 'r') as f:
            data = json.load(f)
            data["stock"].append(item)
        with open(self._stockFile, 'w') as f:
            json.dump(data, f, indent=4)


    def loadData(self) -> list[Any]:
        stockItem = []
        with open(self._stockFile, 'r') as f:
            data = json.load(f)
            for itemData in data["stock"]:
                item: str =  itemData["item"]
                salePrice: float = itemData["sale price"]
                purchasePrice: float = itemData["purchase price"]
                stockQuantity: float = itemData["stock quantity"]

                stockItem.append((item, salePrice, purchasePrice, stockQuantity))
        return stockItem



class TillSettings:
    def __init__(self, dataFile: str) -> None:
        self._settFile = dataFile

        # check for settings file existence
        if os.path.isfile(self._settFile) == True and os.stat(self._settFile).st_size != 0:
            pass
        else:
            self.createNewSettingsFile()


    def createNewSettingsFile(self) -> None:
        with open(self._settFile, 'w') as f:
            writeData = {"settings" : [{
                            "sales tax": 0
                            }]
                        }
            json.dump(writeData, f, indent=4)

    
    def loadSettings(self) -> list[Any]:
        settings: list[Any] = []
        with open(self._settFile, 'r') as f:
            data = json.load(f)
            for item in data["settings"]:
                settings.append(item)
        return settings



class Payments:
    def __init__(self, paymentFile: str) -> None:
        self._paymentFile = paymentFile

        # check for file existence
        if os.path.isfile(self._paymentFile) == True and os.stat(self._paymentFile).st_size != 0:
            pass
        else:
            self.createNewPaymentFile()

        
    def createNewPaymentFile(self) -> None:
        with open(self._paymentFile, 'w') as f:
            writeData = {"Total Payments": 0}
            json.dump(writeData, f, indent=4)

    
    def updateTotalPayments(self, payment: float):
        with open(self._paymentFile, 'r') as f:
            data = json.load(f)
            data["Total Payments"] += payment
        with open(self._paymentFile, 'w') as f:
            json.dump(data, f, indent=4)



if __name__ == '__main__':
    _stockFIle = f'{os.path.dirname(__file__)}\\stock_data.json'
    _settFile = f'{os.path.dirname(__file__)}\\settings.json'
    _paymentFile = f'{os.path.dirname(__file__)}\\payments.json'
    db = StockDatabase(_stockFIle)
    sett = TillSettings(_settFile)
    pay = Payments(_paymentFile)
    Application(database= db, settings= sett, payments= pay).mainloop()
