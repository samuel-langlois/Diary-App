
class User:
    def __init__(self, name):
        self.name = name
        self.password = None

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    def get_name(self):
        return self.name
    
    def save(self):
        file_path = f'userdata/{self.name}.txt'
        with open(file_path, 'w') as f:
        # Save user data to a file
            f.write(f'Name: {self.name}\n')
            f.write(f'Password: {self.password}\n')
    
    @staticmethod
    def load(file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                name = lines[0].split(': ')[1].strip()
                password = lines[1].split(': ')[1].strip()
                return User(name, password)
        except FileNotFoundError:
            print(f"User '{name}' not found.")
            return None

    def __str__(self):
        return f"User(name={self.name}, password={'*' * len(self.password) if self.password else None})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.name == other.name and self.password == other.password
        return False
    