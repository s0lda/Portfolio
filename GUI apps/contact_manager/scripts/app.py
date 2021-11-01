import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from tkinter.constants import CENTER, NO
from typing import Any

class App(tk.Tk):
    def __init__(self, database: Any) -> None:
        super().__init__()
        self._db = database

        self.title('Contact Manager')
        self.iconphoto(True, PhotoImage(file='icons/icon.png'))
        self.geometry('300x300+400+300')
        self.contact_list_panel()

        button_add = ttk.Button(self, text='New contact', command=lambda: self.contact_window('Add New Contact', 'NEW CONTACT'))
        button_add.place(x=10, y=10, width=90, height=30)

        button_edit = ttk.Button(self, text='Edit', command=lambda: self.contact_window('Edit Contact', 'EDIT'))
        button_edit.place(x=10, y=45, width=90, height=30)

        button_delete = ttk.Button(self, text='Delete', command=lambda: self.contact_window('DELETE', 'DELETE'))
        button_delete.place(x=10, y=80, width=90, height=30)

        button_exit = ttk.Button(self, text='Exit', command=self.destroy)
        button_exit.place(x=10, y=260, width=90, height=30)

    def contact_list_panel(self) -> None:
        columns = ('#1')
        self.list_panel = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.list_panel.place(x=115, y=10, width=160, height=280)
        self.list_panel.heading('#1', text='Contacts', anchor=CENTER)
        self.list_panel.column('#1', stretch=NO, width=158)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.list_panel.yview)
        self.list_panel.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=275, y=10, height=280)

        disp_list: list[list[str]] = []
        for contact in self._db.load():
            # display name and surname in contact list
            disp_name = [f'{contact[0].capitalize()} {contact[1].capitalize()}']
            disp_list.append(disp_name)
        for item in sorted(disp_list):
            self.list_panel.insert('', tk.END, values=item)

    # contact window: operation: 'NEW CONTACT", 'DELETE', 'EDIT'
    def contact_window(self, title: str, operation: str) -> None:
        self.cont_win = tk.Toplevel()
        self.cont_win.geometry('300x300+400+300')
        self.cont_win.title(title)

        self.name = StringVar()
        self.surname = StringVar()
        self.mobile = StringVar()
        self.email = StringVar()
        self.dob = StringVar()
        self.address = StringVar()

        # cw for contact window
        cw_accept = ttk.Button(self.cont_win, text='ACCEPT', command=lambda: self.accept_contact(operation))
        cw_accept.place(x=70, y=260, width=60, height=30)

        self.cw_cancel = ttk.Button(self.cont_win, text='CANCEL', command=self.cont_win.destroy, state=tk.NORMAL)
        self.cw_cancel.place(x=160, y=260, width=60, height=30)

        lbl_name = ttk.Label(self.cont_win, text='Name')
        lbl_name.place(x=10, y=10, height=30)
        lbl_surname = ttk.Label(self.cont_win, text='Surname')
        lbl_surname.place(x=10, y=50, height=30)
        lbl_phone = ttk.Label(self.cont_win, text='Mobile')
        lbl_phone.place(x=10, y=90, height=30)
        lbl_email = ttk.Label(self.cont_win, text='Email')
        lbl_email.place(x=10, y=130, height=30)
        lbl_address = ttk.Label(self.cont_win, text='Address')
        lbl_address.place(x=10, y=170, height=30)
        lbl_dob = ttk.Label(self.cont_win, text='Birthday')
        lbl_dob.place(x=10, y=210, height=30)

        ent_name = ttk.Entry(self.cont_win, textvariable=self.name, justify='center')
        ent_name.place(x=130, y=10, height=30, width=150)
        ent_surname = ttk.Entry(self.cont_win, textvariable=self.surname, justify='center')
        ent_surname.place(x=130, y=50, height=30, width=150)
        ent_phone = ttk.Entry(self.cont_win, textvariable=self.mobile, justify='center')
        ent_phone.place(x=130, y=90, height=30, width=150)
        ent_email = ttk.Entry(self.cont_win, textvariable=self.email, justify='center')
        ent_email.place(x=130, y=130, height=30, width=150)
        ent_address = ttk.Entry(self.cont_win, textvariable=self.address, justify='center')
        ent_address.place(x=80, y=170, height=30, width=200)
        ent_dob = ttk.Entry(self.cont_win, textvariable=self.dob, justify='center')
        ent_dob.place(x=130, y=210, height=30, width=150)

        # don't display window for delete function
        if operation == 'DELETE':
            self.accept_contact(operation)
            self.cont_win.destroy()
        elif operation == 'EDIT':
            self.accept_contact(operation)

    def refresh_list_panel(self) -> None:
        self.list_panel.destroy()
        self.contact_list_panel()

    # function for accept button in contact window
    # operation: 'NEW CONTACT", 'DELETE', 'EDIT'
    def accept_contact(self, operation: str) -> None:
        if operation == 'NEW CONTACT':
            if len(self.name.get()) > 0 and self.name.get() != 'YOU NEED A NAME':
                self._db.save([self.name.get().capitalize(), self.surname.get().capitalize(), self.mobile.get(), self.email.get(), self.dob.get(), self.address.get()])
                self.cont_win.destroy()
            else:
                self.name.set('YOU NEED A NAME')
        else:
            current_contact = self.list_panel.focus()
            contact_info = self.list_panel.item(current_contact)
            contact_details: list[Any] = contact_info["values"]
            if operation == 'EDIT':
                self.cw_cancel['state'] = tk.DISABLED
                self.accept_contact(operation='NEW CONTACT')
                for contact in self._db.load():
                    if [f'{contact[0]} {contact[1]}'] == contact_details:
                        # edit_contact.append(contact)                    
                        self.name.set(contact[0].capitalize())
                        self.surname.set(contact[1].capitalize())
                        self.mobile.set(contact[2])
                        self.email.set(contact[3])
                        self.dob.set(contact[4])
                        self.address.set(contact[5])
                self.delete(contact_details)
            else: #'DELETE'
                self.delete(contact_details)
        # update contact list
        self.refresh_list_panel()

    # delete function to use in accept_contact
    def delete(self, contactDetails: list[str]) -> None:
        new_data: list[str] = []
        for contact in self._db.load():
            if [f'{contact[0].capitalize()} {contact[1].capitalize()}'] != contactDetails:
                new_data.append(contact)
        self._db.create_new_file([])
        for contact in new_data:
            self._db.save(contact)

