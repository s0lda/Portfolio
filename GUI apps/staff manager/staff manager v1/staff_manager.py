from json.decoder import JSONDecodeError
import tkinter as tk
from tkinter import StringVar, Toplevel, ttk
import os, json
import copy


class StaffManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.check_save_file()
        self.geometry("1520x600")
        self.title("Staff Manager")
        self.iconbitmap("icon.ico")
        

        self.buttons()
        self.data_view()


    # check if data save file exists and if not create one.
    def check_save_file(self):
        current_path = os.path.dirname(__file__)
        json_file = f'{current_path}\\emp_data.json'
        if os.path.isfile(json_file) == True and os.stat(json_file).st_size != 0:
            pass
        else:
            with open(json_file, 'w+') as f:
                data = {"people": []}
                json.dump(data, f)
    

    def buttons(self):
        # managing buttons, main window
        add = ttk.Button(self, text= 'Add', command= AddNewEmp)
        add.place(x= 10, y= 10, width= 75)
        
        amend = ttk.Button(self, text= 'Amend', command= self.amend)
        amend.place(x= 10, y= 45, width= 75)

        refresh = ttk.Button(self, text= 'Refresh', command= self.update)
        refresh.place(x= 10, y= 80, width= 75)
        
        retire = ttk.Button(self, text= 'Retire', command= self.is_retired)
        retire.place(x= 10, y= 135, width= 75, height= 40)
        
        remove = ttk.Button(self, text= 'Remove', command= self.delete)
        remove.place(x= 10, y= 230, width= 75, height= 40)

        exit_button = ttk.Button(self, text= 'EXIT', command= self.destroy)
        exit_button.place(x= 10, y= 538, width= 75, height= 40)        


    def data_view(self):
        #create columns for tree view
        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.view_panel = ttk.Treeview(self, columns= columns, show= 'headings', height= 27)
        self.view_panel.place(x= 90, y= 10)

        # headings
        self.view_panel.heading('#1', text= 'Name')
        self.view_panel.heading('#2', text= 'Surname')
        self.view_panel.heading('#3', text= 'Position')
        self.view_panel.heading('#4', text= 'DoB')
        self.view_panel.heading('#5', text= 'Start Date')
        self.view_panel.heading('#6', text= 'End Date')
        self.view_panel.heading('#7', text= 'Retired?')

        # set up the scrollbar
        scrollbar = ttk.Scrollbar(self, orient= tk.VERTICAL, command= self.view_panel.yview)
        self.view_panel.configure(yscrollcommand= scrollbar.set)
        scrollbar.place(x= 1495, y= 10, height= 575)

        # insert data
        with open('emp_data.json', 'r') as f:
            empty_file = False
            try:    
                data = json.load(f)
            except JSONDecodeError:
                empty_file = True
                pass
            employees = []
            if empty_file == False:
                
                for item in data["people"]:
                    name = item["name"]
                    surname = item["surname"]
                    position = item["position"]
                    dob = item["dob"]
                    start = item["start"]
                    end = item["end"]
                    retired = item["retired"]

                    employees.append((name, surname, position, dob, start, end, retired))

            # insert all the data to the view panel
            for emp in employees:
                self.view_panel.insert('', tk.END, values= emp)


    # update information on the view panel
    def update(self):
        self.data_view()

    # amend emp data
    def amend(self):
        amend_win = tk.Tk()
        amend_win.geometry('350x250')
        amend_win.title('Amend Employee Details')
        amend_win.iconbitmap('icon.ico')
        
        # cancel button
        def is_cancel():
            amend_win.destroy()
        
        # change button
        def is_amended(to_change, new_personal_data):
            current_item = self.view_panel.focus()
            info = self.view_panel.item(current_item)
            details = info["values"]

            to_remove = {
                "name": str(details[0]),
                "surname": str(details[1]),
                "position": str(details[2]),
                "dob": str(details[3]),
                "start": str(details[4]),
                "end": str(details[5]),
                "retired": str(details[6])
            }
            to_remove = copy.deepcopy(to_remove)

            details_dict = {
                "name": str(details[0]),
                "surname": str(details[1]),
                "position": str(details[2]),
                "dob": str(details[3]),
                "start": str(details[4]),
                "end": str(details[5]),
                "retired": str(details[6])
            }
            
            
            for key, value in details_dict.items():
                if key == to_change:
                    details_dict[f"{to_change}"] = new_personal_data
            
            with open('emp_data.json', 'r') as f:
                data = json.load(f)

                new_data = {
                    "people": []
                }

                for emp_dict in data["people"]:
                    if to_remove != emp_dict:
                        new_data["people"].append(emp_dict)

                new_data["people"].append(details_dict)
                
                with open('emp_data.json', 'w') as f:
                    json.dump(new_data, f, indent= 4)

            amend_win.destroy()
        
        # check if data is not empty, if is: n/a
        def is_empty(data):
            if len(data) == 0:
                return 'n/a'
            else:
                return data


        main_choice_lbl = ttk.Label(amend_win, text= 'What would you like to change?', font= ('Arial', 12))
        main_choice_lbl.place(x= 10, y= 10)

        self.data_options = ('name', 'surname', 'position', 'dob', 'start', 'end')
        self.choice = StringVar()
        options = ttk.OptionMenu(amend_win,
                                self.choice,
                                self.data_options[0],
                                *self.data_options)
        options.place(x= 10, y= 47)
        options.config(width= 15)


        new_emp_data = ttk.Label(amend_win, text= 'New data:', font= ('Arial', 12))
        new_emp_data.place(x= 10, y= 90)


        main_entry = ttk.Entry(amend_win, justify= 'right')
        main_entry.place(x= 10, y= 130)


        ok_button = ttk.Button(amend_win, text= 'CHANGE', command= lambda: is_amended(self.choice.get(), is_empty(main_entry.get())))
        ok_button.place(x= 60, y= 200)

        cancel_button = ttk.Button(amend_win, text= 'CANCEL', command= is_cancel)
        cancel_button.place(x= 150, y= 200)
            

    def delete(self):
        # get the "clicked" emp
        current_item = self.view_panel.focus()
        # get the info of "clicked" emp : dict
        info = self.view_panel.item(current_item)
        # get details of "clicked" emp, "values" are stored emp data : list
        details = info["values"]
        # set the data to json format (need to convert some int to str as program is creating all data as strings)
        details_dict = {
            "name": str(details[0]),
            "surname": str(details[1]),
            "position": str(details[2]),
            "dob": str(details[3]),
            "start": str(details[4]),
            "end": str(details[5]),
            "retired": str(details[6])
        }

        with open('emp_data.json', 'r') as f:
            data = json.load(f)
            
            new_data = {
                "people": []
            }

            for emp_dict in data["people"]:
                if details_dict != emp_dict:
                    new_data['people'].append(emp_dict)

            with open('emp_data.json', 'w') as f:
                json.dump(new_data, f, indent= 4)
        

    def is_retired(self):
        retired_win = tk.Tk()
        retired_win.geometry('280x130')

        # cancel button
        def is_cancel():
            retired_win.destroy()


        def is_ok():
            current_item = self.view_panel.focus()
            info = self.view_panel.item(current_item)
            details = info["values"]

            to_remove = {
                "name": str(details[0]),
                "surname": str(details[1]),
                "position": str(details[2]),
                "dob": str(details[3]),
                "start": str(details[4]),
                "end": str(details[5]),
                "retired": str(details[6])
            }
            to_remove = copy.deepcopy(to_remove)

            details_dict = {
                "name": str(details[0]),
                "surname": str(details[1]),
                "position": str(details[2]),
                "dob": str(details[3]),
                "start": str(details[4]),
                "end": str(details[5]),
                "retired": str(details[6])
            }
            
            
            # for key, value in details_dict.items():
            details_dict["retired"] = "Yes"
            
            with open('emp_data.json', 'r') as f:
                data = json.load(f)

                new_data = {
                    "people": []
                }

                for emp_dict in data["people"]:
                    if to_remove != emp_dict:
                        new_data["people"].append(emp_dict)

                new_data["people"].append(details_dict)
                
                with open('emp_data.json', 'w') as f:
                    json.dump(new_data, f, indent= 4)

            retired_win.destroy()

        ret_lbl = ttk.Label(retired_win, text= "Are you sure you want to RETIRE your employee?")
        ret_lbl.place(x= 10, y= 20)

        ok_button = ttk.Button(retired_win, text= 'RETIRE', command= is_ok)
        ok_button.place(x= 40, y= 60)

        cancel_button = ttk.Button(retired_win, text= 'CANCEL', command= is_cancel)
        cancel_button.place(x= 150, y= 60)
        


class AddNewEmp(Toplevel):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('380x400')
        self.title('Employee Data')
        self.iconbitmap('icon.ico')

        self.labels()
        self.data_entry()


    # set labels
    def labels(self):
        name_lbl = ttk.Label(self, text= 'Name:', font= ('Arial', 12))
        name_lbl.place(x= 10, y= 10)
        
        surname_lbl = ttk.Label(self, text= 'Surname:', font= ('Arial', 12))
        surname_lbl.place(x= 10, y= 50)
        
        position_lbl = ttk.Label(self, text= 'Position:', font= ('Arial', 12))
        position_lbl.place(x= 10, y= 90)
        
        dob_lbl = ttk.Label(self, text= 'Date of Birth:', font= ('Arial', 12))
        dob_lbl.place(x= 10, y= 130)
        
        start_lbl = ttk.Label(self, text= 'Start Date:', font= ('Arial', 12))
        start_lbl.place(x= 10, y= 170)
        
        end_lbl = ttk.Label(self, text= 'End Date:', font= ('Arial', 12))
        end_lbl.place(x= 10, y= 210)
        
        retired_lbl = ttk.Label(self, text= 'Retired?', font= ('Arial', 12))
        retired_lbl.place(x= 10, y= 250)


    # set data entry points
    def data_entry(self):

        def is_empty(data):
            if len(data) == 0:
                return 'n/a'
            else:
                return data

        # accepting details, pressing ok button
        def is_ok():
            # get all the data
            name = is_empty(name_ent.get())
            surname = is_empty(surname_ent.get())
            position = is_empty(position_ent.get())
            dob = is_empty(dob_ent.get())
            start = is_empty(start_ent.get())
            end = is_empty(end_ent.get())
            retired = retired_var.get()
            # append row to the employee data file
            with open('emp_data.json', 'r+') as f:
                data = json.load(f)
           
                new_emp = {
                    "name": name,
                    "surname": surname,
                    "position": position,
                    "dob": dob,
                    "start": start,
                    "end": end,
                    "retired": retired
                }
            
            data["people"].append(new_emp)
            with open('emp_data.json', 'w') as f:    
                json.dump(data, f, indent= 4)
            
            self.destroy()
        
        # cancelation of adding new emp
        def is_cancel():
            self.destroy()


        name_ent = ttk.Entry(self, justify= 'right')
        name_ent.place(x= 215, y= 10)
        
        surname_ent = ttk.Entry(self, justify= 'right')
        surname_ent.place(x= 215, y= 50)
        
        position_ent = ttk.Entry(self, justify= 'right')
        position_ent.place(x= 215, y= 90)
        
        dob_ent = ttk.Entry(self, justify= 'right')
        dob_ent.place(x= 215, y= 130)
        
        start_ent = ttk.Entry(self, justify= 'right')
        start_ent.place(x= 215, y= 170)
        
        end_ent = ttk.Entry(self, justify= 'right')
        end_ent.place(x= 215, y= 210)

        retired_var = StringVar(value= 'No')
        retired_chk = ttk.Checkbutton(
                                        self,
                                        text= 'Yes',
                                        onvalue= 'Yes',
                                        offvalue= 'No',
                                        variable= retired_var)
        retired_chk.place(x= 215, y= 250)


        ok_button = ttk.Button(self, text= 'ADD', command= is_ok)
        ok_button.place(x= 100, y= 350)

        cancel_button = ttk.Button(self, text= 'CANCEL', command= is_cancel)
        cancel_button.place(x= 200, y= 350)

        

if __name__ == "__main__":
    StaffManager().mainloop()
