import json

class users_db:
    def __init__(self):
        with open('app/users.json', 'r') as file:
            self.data = json.load(file)

    def get_data(self) -> dict:
        return self.data

    def set_user_city(self, id, city) -> None:
        self.data[id] = {'city': city}

    def get_user_data(self, id) -> dict:
        return self.data[id]
        
    def get_registred_ids(self) -> list:
        return list(self.data.keys())

    def save(self):
        with open('app/users.json', 'w') as file:
             json.dump(self.data, file)
             file.close()

