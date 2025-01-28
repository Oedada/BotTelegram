import json


class users_db:
    def __init__(self):
        with open('app/users.json', 'r') as file:
            self.data = json.load(file)
            print("init", self.data)
            file.close()

    def get_data(self) -> dict:
        return self.data

    def set_user_param(self, id: str, param: str, value) -> None:
        if id in self.data.keys():
            self.data[id][param] = value
        else:
            self.data[id] = {param: value}
        print("ste_user_param", self.data)

    def get_user_data(self, id) -> dict:
        return self.data[id]

    def save(self) -> None:
        print("save", self.data)
        with open('app/users.json', 'w') as file:
            json.dump(self.data, file)
            file.close()
