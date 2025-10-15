import json
from time import strftime


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


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.my_products = []

    def save_users(self):
        obj = File('users.json')
        list_ = obj.read()
        list_.append(self.__dict__)
        obj.write(list_)

    def check_username(self):
        obj = File('users.json')
        list_ = File('admins.json')
        q = []
        for i in obj.read():
            if self.username == i['username']:
                q.append(False)
                break
        else:
            q.append(True)

        for i in list_.read():
            if self.username == i['username']:
                q.append(False)
                break
        else:
            q.append(True)

        if q[0] == True and q[1] == True:
            return False
        else:
            return True

    def check_login(self, password):
        obj = File('users.json').read()
        for i in obj:
            if i['username'] == self.username and i['password'] == self.password:
                return True
            else:
                return False
        return None

    def user_product(self) -> None:
        user = File('users.json').read()
        for i in user:
            print(*i['my_products'], end='')

    def price(self, amount, id):
        a = False
        products = File('products.json').read()
        users = File('users.json').read()
        my_products = File('my_products.json').read()
        new = {}
        for i in products:
            string = strftime('%Y-%m-%d %H:%M:%S %p')
            if i['id'] == id and i['amount'] >= amount:
                new.update({
                    "name": i["name"],
                    "amount": amount,
                    "id": id,
                    "time": string
                })
                a = True
        if a:
            my_products.append(new)
            File('my_products').write(my_products)
            text = 'sotib olindi'
            print(text.expandtabs(50))
        sum = File('products.json').read()
        for i in sum:
            if i['id'] == id and i['amount'] >= amount:
                i['amount'] -= amount
            elif i['id'] == id and i['amount'] < amount:
                print('bunday miqodrda mahsulot yoq')
            File('products.json').write(sum)
        for j in users:
            if j['username'] == self.username and a:
                j['my_products'].append(new)
        File('users.json').write(users)
