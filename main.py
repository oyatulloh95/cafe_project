import json
from time import strftime
from colorama import Fore


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
            return True
        else:
            return False

    def check_login(self, password):
        obj = File('users.json').read()
        for i in obj:
            if i['username'] == self.username and i['password'] == self.password:
                return True
        return False

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
            File('my_products.json').write(my_products)
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


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.new_products = []

    def save_users(self):
        obj = File('admins.json')
        list_ = obj.read()
        list_.append(self.__dict__)
        obj.write(list_)

    def check_username(self):
        obj = File('admins.json')
        list_ = File('users.json')
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
            return True
        else:
            return False

    def check_login(self, password):
        obj = File('admins.json')
        for i in obj.read():
            if i['username'] == self.username and i['password'] == self.password:
                return True
        else:
            return False

    def user_product(self):
        user = File('admins.json').read()
        for i in user:
            print(*i['new_products'], end='')

    def add_product(self, name, amount, id):
        new = {}
        a = False
        obj = File('products.json').read()
        if amount <= 0:
            print(Fore.RED + "minus son kritmang ")
            return 0
        for i in obj:
            if i['name'] == name:
                print('bunday nomli mahsulot mavjud')
                return
        new.update({
            'id': id,
            'name': name,
            'amount': amount
        })
        obj.append(new)
        File('products.json').write(obj)

        if a:
            obj.append(new)
            File('products.json').write(obj)
            d = 'Mahsulot qushildi'
            print(d.expandtabs(50))
        data = File('admins.json').read()
        for i in data:
            if self.username == i['username'] and self.password == i['password']:
                i['new_products'].append(new)
        File('admins.json').write(data)

    def check_(self, name, amount):
        obj = File('products.json').read()
        for i in obj:
            if i['name'] == name:
                i['amount'] = amount
                File('products.json').write(obj)
                return True
        else:
            return False


def get_id():
    try:
        with open('products.json') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []
    return len(data) + 1


class Product:
    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount
        self.id = get_id()

    def save_product(self):
        products = File('products.json').read()
        products.append(self.__dict__)
        File('products.json').write(products)

    def take_list(self):
        product = File('products.json').read()
        print(Fore.BLUE + '=' * 20 + ' Mahsulotlarimiz ' + Fore.BLUE + '=' * 20)
        for i in product:
            print(Fore.LIGHTYELLOW_EX)
            print("id  :", i["id"], "  ", "name : ", i["name"], "  ", 'number of products', i["amount"])
            print(Fore.BLACK + '=' * 50)


while True:
    print(Fore.YELLOW + '=' * 10, Fore.LIGHTCYAN_EX + 'KAFE ', Fore.YELLOW + '=' * 10)
    print('tanlang>>>')
    text1 = '''    
    1) Login 
    2) Register
    3) chiqish    
    >>>  '''
    check = input(text1)

    if check == '1':
        username = input("Enter username  : ")
        password = input("Enter password  : ")
        user = User(username=username, password=password)
        if user.check_login(password):
            while True:
                print(Fore.YELLOW)
                text2 = '''    
                    1) mahsulotlar
                    2) Men buyurtma qilgan mahsulotlar        
                    3) chiqish                
                    >>>  '''
                check2 = input(text2)
                if check2 == '1':
                    info = Product()
                    info.take_list()
                    print(Fore.LIGHTMAGENTA_EX + " mahsulotlardan tanlang")
                    id = int(input("Product id : "))
                    amount = int(input("Product amount : "))
                    buy = User(username, password)
                    if amount > 0 and id > 0:
                        buy.price(amount, id)
                    else:
                        print(Fore.RED)
                        print("MINUS RAQAM KRITMANG ❌ ")

                if check2 == '2':
                    malumot = User(username=username, password=password)
                    obj = File('users.json').read()
                    for i in obj:
                        if i['username'] == username and i['password'] == password:
                            print(i['my_products'])
                if check2 == '3':
                    print(Fore.MAGENTA + "Kelganingiz uchun rahmat 🙂")
                    break
        user1 = Admin(username=username, password=password)
        if user1.check_login(password):
            while True:
                print('tanlang>>')
                text = Fore.YELLOW + """
                 1)  Sotib olingan mahsulotlar
                 2)  yangi mahsulot qushish
                 3)  mahsulotlar menyusi
                 5)  Chiqish
                >>>>"""
                admin = input(text)
                if admin == '2':
                    name = input('mahsulot nomi : ')
                    amount = int(input('mahsulot soni : '))
                    buy1 = Admin(username, password)
                    a = Admin(username, password)
                    if a.check_(name, amount):
                        buy1.check_(name, amount)
                    if amount > 0:
                        buy = Product(name, amount)
                        buy.save_product()
                        print('mahsulot qushildi🙂')
                    else:
                        print(Fore.RED)
                        print("MINUS RAQAM KRITMANG ❌ ")
                elif admin == '1':
                    data = File('users.json').read()
                    for i in data:
                        print(i)
                elif admin == '3':
                    info = Product()
                    info.take_list()
                elif admin == '5':
                    print(Fore.MAGENTA + "Kelganingiz uchun rahmat 🙂")
                    break
    elif check == '2':
        print(Fore.BLUE)
        username = input("Enter username : ")
        password = input("Enter password : ")
        add = Fore.LIGHTMAGENTA_EX + ''' adminmisiz (ha/ yoq ) '''
        chk1 = input(add)
        if chk1 == 'yoq':
            reg = User(username, password)
            if reg.check_username():
                reg.save_users()
                print("Muvaffaqiyatli Registatsiya")
            else:
                print("Bu username oldin ishlatilgan")
        elif chk1 == 'ha':
            reg1 = Admin(username, password)
            if reg1.check_username():
                reg1.save_users()
                print("Muvaffaqiyatli kirish")
            else:
                print("bu username oldin ishlatilgan")
        else:
            print(Fore.RED + "hato tanlov")
    elif check == '3':
        print('Kelganingiz uchun raxmat 🙂')
        break
    else:
        print(Fore.RED + 'Xato tanlov❌')
