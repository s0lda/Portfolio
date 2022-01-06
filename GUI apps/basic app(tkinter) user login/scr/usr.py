import os
import json

class User:
    def __init__(self, db_path: str) -> None:
        super().__init__()
        self._db_path = db_path
        self.usr_db = f"{self._db_path}\\usr_data.json"

        if os.path.isfile(self.usr_db) and os.stat(self.usr_db).st_size != 0:
            pass
        else:
            self.write_std_usr_db()

    def get_usr_count(self) -> int | None:
        data = self.read_usr_db()
        for key, value in data.items():
            if key == "usr_count":
                return value

    def write_std_usr_db(self) -> None:
        """If user database file is empty or does not exists,
        it will create a standard user file of format 
        
        >>> dict[str, int | list[str]] as .json file.

        {
            "usr_count": 0,
            "users": []
        }"""
        with open(self.usr_db, 'w') as f:
            data: dict[str, int | list[list[str]]] = {
                "usr_count": 0,
                "users": []
            }
            json.dump(data, f, indent=4)

    def read_usr_db(self) -> dict[str, int | list[list[str]]]:
        with open(self.usr_db, 'r') as f:
            data = json.load(f)
        return data

    def write_usr_db(self, db: dict[str, int | list[list[str]]]) -> None:
        with open(self.usr_db, 'w') as f:
            json.dump(db, f, indent= 4)

    def is_login_authorized(self, login: str, password: str) -> bool:
        """Check if login and password are matching."""

        data = self.read_usr_db()
        for item in data["users"]:
            if item[2] == login and item[3] == password:
                return True
        return False

    def create_new_user(self, first_name: str, last_name: str, login: str, password: str) -> None:
        data = self.read_usr_db()
        data["usr_count"] += 1
        new_user: list[str] = [first_name, last_name, login, password]
        data["users"].append(new_user)
        self.write_usr_db(data)

    def is_login_taken(self, login: str) -> bool:
        data = self.read_usr_db()
        for item in data["users"]:
            if item[2] == login:
                return True
        return False

    def is_password_valid(self, password: str) -> bool:
        """Check if password contains at least 3 digits, 1 upper case letter and one special sign.
        Minimum password length is 8."""

        special_signs = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', ',', '.', "'", '"')
        digits: int = 0
        upper_case: int = 0
        lower_case: int = 0
        specials: int = 0
        for i in password:
            if i.isdigit():
                digits += 1
            elif i in special_signs:
                specials += 1
            elif i.isupper():
                upper_case += 1
            else:
                lower_case += 1

        if len(password) >= 8 and digits >= 3 and upper_case >= 1 and specials >= 1:
            return True
        return False
