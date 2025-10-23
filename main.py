import json
from itertools import product
from operator import contains
from time import strftime
from colorama import Fore


class File:
    def __init__(self, filename):
        self.filename = filename
        self.auto_create()

    def auto_create(self):
        try:
            open(self.filename, 'x').close()
            with open(self.filename, 'w') as file:
                json.dump([], file)
        except FileExistsError:
            pass

    def read(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def write(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=3)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.my_products = []

    def save_users(self):
        users = File('users.json').read()
        users.append(self.__dict__)
        File('users.json').write(users)

    def check_username(self):
        users = File('users.json').read()
        admins = File('admins.json').read()
        for u in users + admins:
            if u['username'] == self.username:
                return False
        return True

    def check_login(self):
        users = File('users.json').read()
        for u in users:
            if u['username'] == self.username and u['password'] == self.password:
                return True
        return False

    def price(self, amount, id_):
        products = File('products.json').read()
        users = File('users.json').read()
        my_products = File('my_products.json').read()

        for product in products:
            if product['id'] == id_:
                if product['amount'] < amount:
                    print(Fore.RED + 'Bunday miqdorda mahsulot yo‘q ❌')
                    return
                product['amount'] -= amount
                new = {
                    "name": product["name"],
                    "amount": amount,
                    "price": product["price"],
                    "total": product["price"] * amount,
                    "time": strftime('%Y-%m-%d %H:%M:%S')
                }
                my_products.append(new)
                File('my_products.json').write(my_products)

                for u in users:
                    if u['username'] == self.username:
                        u['my_products'].append(new)
                File('users.json').write(users)
                File('products.json').write(products)
                print(Fore.GREEN + "Sotib olindi ✅")
                return
        print(Fore.RED + 'Mahsulot topilmadi ❌')


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.new_products = []

    def check_login(self):
        admins = File('admins.json').read()
        for a in admins:
            if a['username'] == self.username and a['password'] == self.password:
                return True
        return False

    def add_product(self, name, amount, price):
        if amount <= 0 or price <= 0:
            print(Fore.RED + "Miqdor yoki narx manfiy bo‘lmasin ❌")
            return

        products = File('products.json').read()

        for product in products:
            if product['name'].lower().strip() == name.lower().strip():
                product['amount'] += amount
                product['price'] = price
                File('products.json').write(products)
                print(Fore.GREEN + f"Yangilandi: {name}, +{amount} ta, narx: {price} so‘m")
                return

        new_id = max([p['id'] for p in products], default=0) + 1
        new_product = {"id": new_id, "name": name, "amount": amount, "price": price}
        products.append(new_product)
        File('products.json').write(products)
        print(Fore.GREEN + f"Yangi mahsulot: {name}, {amount} ta, {price} so‘m")

    def show_all_users(self):
        users = File('users.json').read()
        if not users:
            print(Fore.YELLOW + "Foydalanuvchilar hali yo‘q.")
            return
        for u in users:
            print(Fore.CYAN + f"{u['username']} → {len(u['my_products'])} ta mahsulot sotib olgan")

    def show_statistics(self):
        users = File('users.json').read()
        all_sales = []
        total_sold = 0

        for u in users:
            for p in u['my_products']:
                all_sales.append(p)
                total_sold += p['amount']

        print(Fore.CYAN + "\n========== STATISTIKA ==========")
        print(Fore.YELLOW + f"Jami sotilgan mahsulotlar soni: {len(all_sales)}")
        print(Fore.YELLOW + f"Umumiy miqdor: {total_sold} dona\n")

        product_count = {}
        for p in all_sales:
            name = p['name']
            product_count[name] = product_count.get(name, 0) + p['amount']
        sorted_products = sorted(product_count.items(), key=lambda x: x[1], reverse=True)
        print(Fore.GREEN + "Eng ko‘p sotilgan mahsulotlar:")
        for name, count in sorted_products[:3]:
            print(f"{name}: {count} dona")

        user_activity = {}
        for u in users:
            user_activity[u['username']] = sum(p['amount'] for p in u['my_products'])
        sorted_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)

        print(Fore.MAGENTA + "\nEng faol foydalanuvchilar:")
        for name, count in sorted_users[:3]:
            print(f"{name}: {count} dona mahsulot")
        print(Fore.CYAN + "================================\n")


class Product:
    def take_list(self):
        products = File('products.json').read()
        print(Fore.BLUE + '=' * 20 + ' Mahsulotlarimiz ' + '=' * 20)
        if not products:
            print(Fore.YELLOW + "Mahsulotlar hali mavjud emas.")
            return []
        for p in products:
            print(Fore.LIGHTYELLOW_EX + f"id: {p['id']} | {p['name']} | {p['amount']} dona | {p['price']} so‘m")
            # print(Fore.BLACK + '=' * 50)


default_admin = {"username": "admin", "password": "1234", "new_products": []}
admins_data = File('admins.json').read()
if not any(a['username'] == 'admin' for a in admins_data):
    admins_data.append(default_admin)
    File('admins.json').write(admins_data)

while True:
    print(Fore.YELLOW + '=' * 10, Fore.LIGHTCYAN_EX + 'KAFE', Fore.YELLOW + '=' * 10)
    print("Tanlang>>>")
    text1 = """
    1) Login 
    2) Register
    3) Chiqish
    >>> """
    check = input(text1)

    if check == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = User(username, password)
        admin = Admin(username, password)

        if user.check_login():
            while True:
                text2 = """
                    1) Mahsulotlar
                    2) Mening buyurtmalarim        
                    3) Chiqish                
                    >>> """
                check2 = input(text2)
                if check2 == '1':
                    info = Product()
                    products = info.take_list()
                    if not products:
                        continue
                    id_ = int(input("Mahsulot ID: "))
                    amount = int(input("Miqdor: "))
                    if amount>0:
                        user.price(amount, id_)
                    else:
                        print(Fore.RED + "Minus yoki 0 kiritmang ❌")
                elif check2 == '2':
                    data = File('users.json').read()
                    for u in data:
                        if u['username'] == username:
                            if not u['my_products']:
                                print(Fore.YELLOW + "Siz hali hech narsa sotib olmadingiz.")
                                break
                            print(Fore.CYAN + "\n" + "=" * 40)
                            print(Fore.LIGHTWHITE_EX + "          ☕ CAFE RECEIPT ☕")
                            print(Fore.CYAN + "=" * 40)
                            total_sum = 0
                            for item in u['my_products']:
                                print(
                                    Fore.WHITE + f"{item['name']} x {item['amount']} | {item['price']} so‘m | Jami: {item['total']} so‘m")
                                total_sum += item['total']
                            print(Fore.CYAN + "--------------------------")
                            print(Fore.GREEN + f"Umumiy summa: {total_sum} so‘m")
                            print(Fore.CYAN + "==========================\n")
                            break
                elif check2 == '3':
                    print(Fore.MAGENTA + "Kelganingiz uchun rahmat 🙂")
                    break

        elif admin.check_login():
            while True:
                text = """
                 1) Foydalanuvchilar ro‘yxati
                 2) Yangi mahsulot qo‘shish
                 3) Mahsulotlar menyusi
                 4) Statistika
                 5) Chiqish
                >>> """
                adm = input(text)
                if adm == '1':
                    admin.show_all_users()
                elif adm == '2':
                    name = input('Mahsulot nomi: ')
                    amount = int(input('Miqdor: '))
                    price = int(input('Narx (so‘m): '))
                    admin.add_product(name, amount, price)
                elif adm == '3':
                    info = Product()
                    info.take_list()
                elif adm == '4':
                    admin.show_statistics()
                elif adm == '5':
                    print(Fore.MAGENTA + "Kelganingiz uchun rahmat 🙂")
                    break
        else:
            print(Fore.RED + "Login yoki parol noto‘g‘ri ❌")

    elif check == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        reg = User(username, password)
        if reg.check_username():
            reg.save_users()
            print(Fore.GREEN + "Muvaffaqiyatli ro‘yxatdan o‘tildi ✅")
        else:
            print(Fore.RED + "Bu username allaqachon ishlatilgan ❌")

    elif check == '3':
        print(Fore.MAGENTA + "Kelganingiz uchun rahmat 🙂")
        break
    else:
        print(Fore.RED + "Xato tanlov ❌")
