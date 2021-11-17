import tkinter as tk
from tkinter import DoubleVar, Frame, PhotoImage, StringVar, ttk
from tkinter.constants import NO
from typing import Any
import tkcalendar
from functools import partial

from scripts.database import Database

class App(tk.Tk):
    def __init__(self, database: Database, resources: str) -> None:
        super().__init__()
        self.db = database
        self._res = resources
        # Variable to transfer data between MainFrame and AddHolidayFrame, ManageEmployeeFrame
        self.emp_name = StringVar()
        self.emp_hol_all = DoubleVar()

        # Getting centre of the screen.
        self.screensize = self._get_screen_size()
        scr_center_x = round((self.screensize[0] / 2) - 250)
        scr_center_y = round((self.screensize[1] / 2) - 250)

        # Configure Window.
        self.geometry(f'500x500+{scr_center_x}+{scr_center_y}')
        self.title('Holiday Manager')
        self.iconphoto(True, PhotoImage(file=f'{self._res}\\icon.png'))
        self.resizable(True, True)
        
        # Setting starting frame.
        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class: Any) -> None:
        new_frame: Frame = frame_class(self)
        self.frame = new_frame
        self.frame.place(relheight=1, relwidth=1, relx=0, rely=0)

    def _get_screen_size(self) -> tuple[float, float]:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height

class MainFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self.data_view(parent)

        add_new = ttk.Button(self, text='Add New Employee', command=lambda: parent.switch_frame(AddEmployeeFrame))
        add_new.place(relheight=0.2, relwidth=0.3, relx=0.001, rely=0.001)
        add_hol = ttk.Button(self, text='Add Holiday', command=lambda: self._btn_function(parent, AddHolidayFrame))
        add_hol.place(relheight=0.2, relwidth=0.3, relx=0.001, rely=0.202)
        mng_emp = ttk.Button(self, text='Manage Employee', command=lambda: self._btn_function(parent, ManageEmployeeFrame))
        mng_emp.place(relheight=0.2, relwidth=0.3, relx=0.001, rely=0.403)

    def data_view(self, parent: App) -> None:
        columns = ('#1', '#2')
        self.emp_list = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.emp_list.place(relheight=0.99, relwidth=0.69, relx=0.303, rely=0.002)
        self.emp_list.heading('#1', text='Name')
        self.emp_list.heading('#2', text='Holiday Left')
        self.emp_list.column('#1', anchor='center', stretch=NO, width=200)
        self.emp_list.column('#2', anchor='center', stretch=NO, width=140)

        for item in parent.db.load():
            name: str = item[0]
            holiday_left: float = item[1] - item[2]
            self.emp_list.insert('', tk.END, values=[name, holiday_left])

    def _btn_function(self, parent: App, frame: type) -> None:
        # Get details for employee.
        current_item = self.emp_list.focus()
        info = self.emp_list.item(current_item)
        details: Any = info["values"]
        # Prevent going in to add holiday without choosing employee.
        if len(details) > 0:
            parent.emp_name.set(details[0])
            parent.emp_hol_all.set(details[1])
            parent.switch_frame(frame)
        # Set pop up window with an error message.
        else:
            err_win = tk.Toplevel()
            err_win.title('Error')
            screen_x = round((parent.screensize[0] / 2) - 150)
            screen_y = round((parent.screensize[1] / 2) - 90)
            err_win.geometry(f'300x180+{screen_x}+{screen_y}')
            lbl = ttk.Label(err_win, text='Please choose employee first.', anchor='center', font=('Helvetica', 12, 'bold'))
            lbl.place(relheight=0.4, relwidth=0.8, relx=0.1, rely=0.1)
            btn = ttk.Button(err_win, text='OK', command=err_win.destroy)
            btn.place(relheight=0.2, relwidth=0.4, relx=0.3, rely=0.5)

class AddEmployeeFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self.name = StringVar()
        self.hours = StringVar()

        label = partial(ttk.Label, self, font=('Helvetica', 10, 'bold'), anchor='center')
        entry = partial(ttk.Entry, self, justify='center')

        name_lbl = label(text='Name')
        name_lbl.place(relheight=0.1, relwidth=0.3, relx=0.001, rely=0.1)
        name_ent = entry(textvariable=self.name)
        name_ent.place(relheight=0.1, relwidth=0.5, relx=0.497, rely=0.1)
        hol_all_lbl = label(text='Holiday Allowance')
        hol_all_lbl.place(relheight=0.1, relwidth=0.45, relx=0.001, rely=0.205)
        hours_ent = entry(textvariable=self.hours)
        hours_ent.place(relheight=0.1, relwidth=0.5, relx=0.497, rely=0.205)

        add_btn = ttk.Button(self, text='Add', command=lambda: self.add_new_emp(parent))
        add_btn.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.7)
        cancel_btn = ttk.Button(self, text='Cancel', command=lambda: parent.switch_frame(MainFrame))
        cancel_btn.place(relheight=0.1, relwidth=0.2, relx=0.6, rely=0.7)
    
    def add_new_emp(self, parent: App) -> None:
        names_of_emps: list[str] = []
        for employee in parent.db.load():
            names_of_emps.append(employee[0])
        if self.name.get() in names_of_emps:
            self.name.set('This name is already in your database.')
        else:
            # Check if name field is not empty and holiday allowance is digits.
            if len(self.name.get()) > 0 and self.name.get() != 'You need a name here.' and self.name.get() != 'This name is already in your database.':
                if self.hours.get().isdigit():
                    new_emp = [self.name.get(), float(self.hours.get()), 0]
                    parent.db.create_emp(new_emp)
                    parent.switch_frame(MainFrame)
                else:
                    self.hours.set('You need a number here.')
            else:
                self.name.set('You need a name here.')

class AddHolidayFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self.data_view()
        self.day_type = StringVar(value='Full')
        self.hol_all = DoubleVar(value=parent.emp_hol_all.get())
        self.hol_used = DoubleVar()

        label = partial(ttk.Label, self, font=('Helvetica', 10, 'bold'), anchor='center')

        add_btn = ttk.Button(self, text='Add', command=lambda: self.add_date_view_panel(parent))
        add_btn.place(relheight=0.1, relwidth=0.2, relx=0.505, rely=0.503)

        remove_btn = ttk.Button(self, text='Remove', command=self.remove_from_view_panel)
        remove_btn.place(relheight=0.1, relwidth=0.2, relx=0.798, rely=0.503)

        full_day = ttk.Radiobutton(self, text='Full Day', variable=self.day_type, value='Full')
        full_day.place(relheight=0.1, relwidth=0.15, relx=0.05, rely=0.5)
        half_day = ttk.Radiobutton(self, text='Half Day', variable=self.day_type, value='Half')
        half_day.place(relheight=0.1, relwidth=0.15, relx=0.2, rely=0.5)
        finish_btn = ttk.Button(self, text='Finish', command=lambda: self.accept_holiday(parent))
        finish_btn.place(relheight=0.15, relwidth=0.25, relx=0.2, rely=0.8)
        cancel_btn = ttk.Button(self, text='Cancel', command=lambda: parent.switch_frame(MainFrame))
        cancel_btn.place(relheight=0.15, relwidth=0.25, relx=0.6, rely=0.8)
        current_emp = label(textvariable=parent.emp_name)
        current_emp.place(relheight=0.1, relwidth=0.4, relx=0.01, rely=0.6)
        allowance_lbl = label(text='Available:')
        allowance_lbl.place(relheight=0.1, relwidth=0.3, relx=0.01, rely=0.7)
        allowance_var = label(textvariable=self.hol_all)
        allowance_var.place(relheight=0.1, relwidth=0.2, relx=0.3, rely=0.7)

        self.calendar = tkcalendar.Calendar(self, state='normal',
                                             weekendays=[6,7],
                                             firstweekday='monday',
                                             selectmode='day')
        self.calendar.place(relheight=0.5, relwidth=0.5, relx=0.001, rely=0.001)

    def data_view(self) -> None:
        columns = ('#1', '#2')
        self.view_panel = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.view_panel.place(relheight=0.5, relwidth=0.490, relx=0.505, rely=0.001)
        self.view_panel.heading('#1', text='Date')
        self.view_panel.heading('#2', text='Type')
        self.view_panel.column('#1', anchor='center', stretch=NO, width=150)
        self.view_panel.column('#2', anchor='center', stretch=NO, width=80)

    def add_date_view_panel(self, parent: App) -> None:
        # Prevent adding the same date multiple times.
        # Only once the date can be added no matter whether is Full or Half day.
        # If Half Day is added but want to change it to full, first need to remove the date
        # from the list, then re add it as a Full Day.
        date: Any = self.calendar.get_date()
        type = self.day_type.get()
        if len(self.view_panel.get_children()) == 0:
            self.view_panel.insert('', tk.END, values=[date, type])
        else:
            list_of_dates: list[str] = []
            for child in self.view_panel.get_children():
                list_of_dates.append(self.view_panel.item(child, 'values')[0])
            if date in list_of_dates:
                pass
            else:
                self.view_panel.insert('', tk.END, values=[date, type])
        # Update holiday allowance on screen.
        self.calculate_hol_allowance(parent)
            
    def remove_from_view_panel(self) -> None:
        # except IndexError for deleting when list is empty
        try:
            selected_item = self.view_panel.selection()[0]
            self.view_panel.delete(selected_item)
        except IndexError:
            pass

    def calculate_hol_allowance(self, parent: App) -> None:
        allowance = parent.emp_hol_all.get()
        field_count = 0.0
        for child in self.view_panel.get_children():
            if self.view_panel.item(child, 'values')[1] == 'Full':
                field_count += 1
            elif self.view_panel.item(child, 'values')[1] == 'Half':
                field_count += 0.5
        hol_left = allowance - field_count
        # Set on screen update.
        self.hol_all.set(hol_left)
        tot_hol_used = allowance - self.hol_all.get()
        self.hol_used.set(tot_hol_used)

    def accept_holiday(self, parent: App) -> None:
        # Finish Button Function
        # The only one way to accept holiday, and update database.
        name: str = parent.emp_name.get()
        hol_used: float = self.hol_used.get()
        new_emp_data: list[Any] = []

        new_data: list[Any] = []
        for item in parent.db.load():
            if item[0] != name:
                new_data.append(item)
            else:
                new_emp_data = list(item)
        # Change holiday used value to a new one.
        new_emp_data[2] =  new_emp_data[2] + hol_used
        new_data.append(new_emp_data)
        parent.db.create_emp_file([])

        for item in new_data:
            parent.db.create_emp(item)
        # Switch back to MainFrame after adding holidays
        parent.switch_frame(MainFrame)

class ManageEmployeeFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self.name = StringVar()
        self.hol_allowance = StringVar()
        self.hol_used = StringVar()

        label = partial(ttk.Label, self, font=('Helvetica', 10, 'bold'), anchor='center')
        entry = partial(ttk.Entry, self, justify='center')

        name_lbl = label(text='Name')
        name_lbl.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.05)
        name_ent = entry(textvariable=self.name)
        name_ent.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.15)
        allowance_ent = label(text='Holiday Allowance')
        allowance_ent.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.25)
        all_var = entry(textvariable=self.hol_allowance)
        all_var.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.35)
        used_hol = label(text='Used Holiday')
        used_hol.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.45)
        used_var = entry(textvariable=self.hol_used)
        used_var.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.55)

        accept_btn = ttk.Button(self, text='Accept', command=lambda: self.accept_changes(parent))
        accept_btn.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.7)

        cancel_btn = ttk.Button(self, text='Cancel', command=lambda: parent.switch_frame(MainFrame))
        cancel_btn.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.7)

        remove_btn = ttk.Button(self, text='Delete Employee', command=lambda: self.remove_emp(parent))
        remove_btn.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.7)

        self.before_details: list[Any] = []

        for item in parent.db.load():
            if parent.emp_name.get() == item[0]:
                self.name.set(item[0])
                self.hol_allowance.set(item[1])
                self.hol_used.set(item[2])
                for i in item:
                    self.before_details.append(i)
        print(self.before_details)

    def accept_changes(self, parent: App) -> None:
        if self.check_for_empty_fields(parent) == True:
            emp_data: list[Any] = []
            for item in parent.db.load():
                if list(item) != self.before_details:
                    emp_data.append(item)

            new_emp_details = [self.name.get(), float(self.hol_allowance.get()), float(self.hol_used.get())]
            emp_data.append(new_emp_details)
            parent.db.create_emp_file([])
            for item in emp_data:
                parent.db.create_emp(item)
            parent.switch_frame(MainFrame)

    def check_for_empty_fields(self, parent: App) -> bool:
        # Very basic check for empty entry fields.
        data_filled = False
        field_count = 0
        if len(self.name.get()) < 2:
            self.name.set('You need a name here. At least 2 characters.')
        else:
            field_count += 1
        try:
            if float(self.hol_allowance.get()) > 0:
                field_count += 1
        except ValueError:
            self.hol_allowance.set('You need a Value here.')
        try:
            if float(self.hol_used.get()) >= 0:
                field_count += 1
            else:
                self.hol_used.set(self.before_details[2])
        except ValueError:    
            self.hol_used.set(self.before_details[2])

        if field_count == 3:
            data_filled = True
        print(f'Data Filled: {data_filled}')
        return data_filled

    def remove_emp(self, parent: App) -> None:
        emp_data: list[Any] = []
        for item in parent.db.load():
            if list(item) != self.before_details:
                emp_data.append(item)
        parent.db.create_emp_file([])
        for item in emp_data:
            parent.db.create_emp(item)
        parent.switch_frame(MainFrame)