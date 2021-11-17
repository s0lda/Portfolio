import os, json
from typing import Any

class Database:
    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path

        self.emp_path = f'{self._path}\\emp_data.json'

        try:
            os.makedirs(self._path)
            print(f'Created: {self._path}')
        except FileExistsError:
            print(f'Checked: {self._path}')

        if os.path.isfile(self.emp_path) == True and os.stat(self.emp_path).st_size != 0:
            pass
        else:
            self.create_emp_file([])

    def create_emp_file(self, employee: list[Any]) -> None:
        with open(self.emp_path, 'w') as f:
            data = {"people": employee}
            json.dump(data, f, indent=4)

    def create_emp(self, employee: list[Any]) -> None:
        new_emp = {
            "name": employee[0],
            "hol allowance": employee[1],
            "hol used": employee[2]
        }

        with open(self.emp_path, 'r') as f:
            data = json.load(f)
            data["people"].append(new_emp)
        with open(self.emp_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load(self) -> list[Any]:
        employees: list[Any] = []
        with open(self.emp_path, 'r') as f:
            data = json.load(f)
            for item in data["people"]:
                name = item["name"]
                hol_all = item["hol allowance"]
                hol_used = item["hol used"]

                employees.append((name, hol_all, hol_used))
        return employees