import json


class File:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as file:
            try:
                list_ = json.load(file)
            except json.decoder.JSONDecodeError:
                list_ = []
        return list_

    def write(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=3)
