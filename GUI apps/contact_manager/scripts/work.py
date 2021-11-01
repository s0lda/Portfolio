import os, json

class ContactDB:
    def __init__(self, database: str) -> None:
        super().__init__()
        self._db = database

        if os.path.isfile(self._db) and os.stat(self._db).st_size != 0:
            pass
        else:
            self.create_new_file([])

    def create_new_file(self, contacts: list[str]) -> None:
        with open(self._db, 'w') as f:
            data = {"contacts": contacts}
            json.dump(data, f, indent=4)

    def load(self) -> list[str]:
        contacts_list: list[str] = []
        with open(self._db, 'r') as f:
            data = json.load(f)
            for item in data["contacts"]:
                contacts_list.append(item)
        return contacts_list

    def save(self, contact: list[str]) -> None:
        with open(self._db, 'r') as f:
            data = json.load(f)
            data["contacts"].append(contact)
        with open(self._db, 'w') as f:
            json.dump(data, f, indent=4)
