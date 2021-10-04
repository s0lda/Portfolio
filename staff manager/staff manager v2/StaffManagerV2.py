import json
from os import path
import tkinter as tk
from tkinter import StringVar, ttk
import os
from tkinter.constants import CENTER, NO
from ttkbootstrap import Style


class Window(tk.Tk):
    def __init__(self, database: object) -> None:
        super().__init__()
        self._db = database

        self.geometry('1000x500')
        self.title('Staff Manager')
        self.iconbitmap('icon.ico')
        self.buttons()
        self.data_view()
        
        # set theme for the app (from ttkbootstrap)
        style = Style(theme='darkly')
        self = style.master


    def buttons(self) -> None:
        # managing buttons, main window
        add = ttk.Button(self, text='Add', command=self.add_new_emp)
        add.place(x=10, y=10, width=75, height=40)

        amend = ttk.Button(self, text='Amend', command=self.amend_emp)
        amend.place(x=10, y=55, width=75, height=40)

        retire = ttk.Button(self, text='Retire', command=self.retire_emp)
        retire.place(x=10, y=100, width=75, height=40)

        remove = ttk.Button(self, text='Remove', command=self.delete_emp)
        remove.place(x=10, y=180, width=75, height=40)

        exit_button = ttk.Button(self, text= 'EXIT', command=self.destroy)
        exit_button.place(x=10, y=450, width=75, height=40)

    
    def data_view(self) -> None:
        # create columns
        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.view_panel = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.view_panel.place(x=90, y=10, width=890, height=480)

        # headings
        self.view_panel.heading('#1', text='Name')
        self.view_panel.heading('#2', text='Surname')
        self.view_panel.heading('#3', text='Position')
        self.view_panel.heading('#4', text='DoB')
        self.view_panel.heading('#5', text='Start Date')
        self.view_panel.heading('#6', text='End Date')
        self.view_panel.heading('#7', text='Retired?')
        
        # set colums properties
        self.view_panel.column('#1', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#2', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#3', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#4', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#5', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#6', anchor=CENTER, stretch=NO, width=135)
        self.view_panel.column('#7', anchor=CENTER, stretch=NO, width=80)
        
        # set scrollbal for view panel
        scrollbar = ttk.Scrollbar(self, orient= tk.VERTICAL, command= self.view_panel.yview)
        self.view_panel.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=980, y=10, width=20, height=480)

        for emp in EmployeeDatabase.load(self._db):
            self.view_panel.insert('', tk.END, values=emp)


    def refresh_view_panel(self) -> None:
        self.view_panel.destroy()
        self.data_view()


    def add_new_emp(self) -> None:
        new_emp_win = tk.Toplevel(self)
        new_emp_win.geometry('380x400')
        new_emp_win.title('Add New Employee')
        new_emp_win.iconbitmap('icon.ico')


        def check_empty_entry(data: str) -> str:
            if len(data) == 0:
                return 'n/a'
            else:
                return data


        def accept_new_emp() -> None:
            # get all the data
            name = check_empty_entry(name_ent.get())
            surname = check_empty_entry(surname_ent.get())
            position = check_empty_entry(position_ent.get())
            dob = check_empty_entry(dob_ent.get())
            start = check_empty_entry(start_ent.get())
            end = check_empty_entry(end_ent.get())
            retired = retired_var.get()

            new_emp = [name, surname, position, dob, start, end, retired]
            EmployeeDatabase.save(self._db, employees=new_emp)
            
            new_emp_win.destroy()
            self.refresh_view_panel()
            

        # set labels for Add New Emp window
        name_lbl = ttk.Label(new_emp_win, text='Name:', font=('Arial', 12))
        name_lbl.place(x=10, y=10)

        surname_lbl = ttk.Label(new_emp_win, text='Surname:', font=('Arial', 12))
        surname_lbl.place(x=10, y=50)

        position_lbl = ttk.Label(new_emp_win, text='Position:', font=('Arial', 12))
        position_lbl.place(x=10, y=90)

        dob_lbl = ttk.Label(new_emp_win, text='Date of Birth:', font=('Arial', 12))
        dob_lbl.place(x=10, y=130)

        start_lbl = ttk.Label(new_emp_win, text='Start Date:', font=('Arial', 12))
        start_lbl.place(x=10, y=170)

        end_lbl = ttk.Label(new_emp_win, text='End Date:', font=('Arial', 12))
        end_lbl.place(x=10, y=210)

        retired_lbl = ttk.Label(new_emp_win, text='Retired?', font=('Arial', 12))
        retired_lbl.place(x=10, y=250)

        # set entry points for data
        name_ent = ttk.Entry(new_emp_win, justify='right')
        name_ent.place(x=215, y=10)
        
        surname_ent = ttk.Entry(new_emp_win, justify='right')
        surname_ent.place(x=215, y=50)
        
        position_ent = ttk.Entry(new_emp_win, justify='right')
        position_ent.place(x=215, y=90)
        
        dob_ent = ttk.Entry(new_emp_win, justify='right')
        dob_ent.place(x=215, y=130)
        
        start_ent = ttk.Entry(new_emp_win, justify='right')
        start_ent.place(x=215, y=170)
        
        end_ent = ttk.Entry(new_emp_win, justify='right')
        end_ent.place(x=215, y=210)

        retired_var = StringVar(value='No')
        retired_chk = ttk.Checkbutton(
                                        new_emp_win,
                                        text='Yes',
                                        onvalue='Yes',
                                        offvalue='No',
                                        variable=retired_var)
        retired_chk.place(x=215, y=250)


        ok_button = ttk.Button(new_emp_win, text='ADD', command=accept_new_emp)
        ok_button.place(x=100, y=350)

        cancel_button = ttk.Button(new_emp_win, text='CANCEL', command=new_emp_win.destroy)
        cancel_button.place(x=200, y=350)


    def delete_emp(self) -> None:
        # get "clicked" emp
        current_emp = self.view_panel.focus()
        emp_info = self.view_panel.item(current_emp)
        emp_details = emp_info["values"]
        # need it as tuple for 'for loop' comparison
        emp_details = tuple(emp_details)

        # delete emp
        new_data = []
        for employee in EmployeeDatabase.load(self._db):
            if employee != emp_details:
                new_data.append(employee)

        EmployeeDatabase.create_new(self._db, [])
        
        for emp in new_data:
            EmployeeDatabase.save(self._db, emp)
        # update view panel
        self.refresh_view_panel()


    def change_details(self, change_detail_index: int, new_detail: str) -> None:
        # get 'clicked' emp
        current_emp = self.view_panel.focus()
        emp_info = self.view_panel.item(current_emp)
        details = emp_info["values"]
        # need it as tuple for 'for loop' comparison
        details_tup = tuple(details)

        emp_to_change = details

        # copy rest of emps
        new_data = []
        for employee in EmployeeDatabase.load(self._db):
            if employee != details_tup:
                new_data.append(employee)

        # append emp with changed detail
        details[change_detail_index] = new_detail
        new_data.append(details)

        EmployeeDatabase.create_new(self._db, [])
        # write to database
        for emp in new_data:
            EmployeeDatabase.save(self._db, emp)
            
        self.refresh_view_panel()



    def amend_emp(self) -> None:
        amend_win = tk.Toplevel()
        amend_win.geometry('250x250')
        amend_win.title('Amend Employee Details')
        amend_win.iconbitmap('icon.ico')

        
        # check if data is not empty, if is: n/a
        def is_empty(data: str) -> str:
            if len(data) == 0:
                return 'n/a'
            else:
                return data

    
        main_choice_lbl = ttk.Label(amend_win, text='What would you like to change?', font=('Arial', 12))
        main_choice_lbl.place(x=10, y=10)

        self.data_options = ('Name', 'Surname', 'Position', 'DoB', 'Start', 'End')
        self.choice = StringVar()
        options = ttk.OptionMenu(amend_win,
                                self.choice,
                                self.data_options[0],
                                *self.data_options)
        options.place(x=10, y=47)
        options.config(width=15)

        new_emp_data = ttk.Label(amend_win, text='New data:', font=('Arial', 12))
        new_emp_data.place(x=10, y=90)


        main_entry = ttk.Entry(amend_win, justify='right')
        main_entry.place(x=10, y=130)


        ok_button = ttk.Button(amend_win, text='CHANGE', command=lambda: [self.change_details(self.data_options.index(self.choice.get()), is_empty(main_entry.get())), amend_win.destroy()])
        ok_button.place(x=60, y=200)

        cancel_button = ttk.Button(amend_win, text='CANCEL', command=amend_win.destroy)
        cancel_button.place(x=150, y=200)


    def retire_emp(self) -> None:
        retired_win = tk.Toplevel()
        retired_win.geometry('280x130')

        ret_lbl = ttk.Label(retired_win, text="Are you sure you want to RETIRE your employee?")
        ret_lbl.place(x=10, y=20)
        
        ok_button = ttk.Button(retired_win, text='RETIRE', command=lambda: [self.change_details(6, "Yes"), retired_win.destroy()])
        ok_button.place(x=40, y=60)

        cancel_button = ttk.Button(retired_win, text='CANCEL', command=retired_win.destroy)
        cancel_button.place(x=150, y=60)



class EmployeeDatabase:
    def __init__(self, json_file: str) -> None:
        self._file = json_file
        

        if os.path.isfile(json_file) == True and os.stat(json_file).st_size != 0:
            pass
        else:
            self.create_new([])


    def load(self) -> list[str]:
        employees: list[str] = []
        with open(self._file, 'r') as f:
            data = json.load(f)
            for item in data["people"]:
                name: str = item["name"]
                surname: str = item["surname"]
                position: str = item["position"]
                dob: str = item["dob"]
                start: str = item["start"]
                end: str = item["end"]
                retired: str = item["retired"]
                
                employees.append((name, surname, position, dob, start, end, retired))
        return employees
    
    
    def create_new(self, employees: list) -> None:
        with open(self._file, 'w') as f:
            data = {"people": employees}
            json.dump(data, f, indent=4)


    def save(self, employees: list[str]) -> None:
        new_emp = {
                    "name": employees[0],
                    "surname": employees[1],
                    "position": employees[2],
                    "dob": employees[3],
                    "start": employees[4],
                    "end": employees[5],
                    "retired": employees[6]
                }
        with open(self._file, 'r') as f:
            data = json.load(f)
            data["people"].append(new_emp)
        with open(self._file, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    path = f'{os.path.dirname(__file__)}\\emp_db.json'
    db = EmployeeDatabase(path)
    Window(database= db).mainloop()
