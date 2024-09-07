from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import datetime
import time
import os
import base64

class App:
    def __init__(self):
        gen = RSA.generate(3072)
        self.private_key = gen.export_key()
        self.public_key = gen.public_key().export_key()

        self.page_choice = None

    def startup(self):
        print('\tWelcome to this Task Tracking app\nThis can help you track what you want to do and your progess')
        print("Let's get started")
        print('Log in to continue your journey')
        print("\nDon't have a account? Register to start the journey!")
        choice = input('Enter your choice\n<log> for log in\n<reg> for register -> ')
        if choice == 'log':
            os.system("cls")
            self.login()
        
        elif choice == 'reg':
            os.system("cls")
            self.register()

        else:
            os.system("cls")
            print('Command is not found. Please try again!')
            time.sleep(2)
            os.system("cls")
            self.startup()

    def login(self):
        self.username = input('Please enter your username -> ')
        password = input('Please enter your password -> ')

        try:
            with open(self.username + ".txt", "r", encoding="utf-8-sig") as f:
                for i in f:
                    acc = i.split()
            check_username = acc[0]
            enc_password = base64.b64decode(acc[1])

            with open(self.username + "key.pem", "rb") as f:
                pkey = f.read()

            key = RSA.import_key(pkey)
            cipher = PKCS1_OAEP.new(key)
            dec = cipher.decrypt(enc_password)
            
            check_password = dec.decode("utf-8")
            if check_username == self.username and check_password == password:
                print('Successfully signed in')
                time.sleep(2)
                os.system("cls")     
                self.mainpage()

            else:
                print('User is not found')
                print('Please check your username / password')
                time.sleep(2)
                os.system("cls")
                self.login()
            
        except FileNotFoundError:
            os.system("cls")
            print('User file is not found')
            print('Please check your username / password')
            time.sleep(2)
            os.system("cls")
            self.startup()

    def register(self):
        self.username = input('Please enter username -> ')
        password = input('Please enter password -> ')

        byte_password = password.encode("utf-8")

        key = RSA.import_key(self.public_key)
        cipher = PKCS1_OAEP.new(key)
        enc_password = cipher.encrypt(byte_password)

        with open(self.username + "key.pem", "wb") as f:
            f.write(self.private_key)

        join = datetime.datetime.now()
        with open(self.username + "info.txt", "w", encoding="utf-8") as f:
            f.write('Name: ' + self.username + '\n' + 'Password: <CLASSIFIED>' + '\n' + 'Date joined: ' + join.strftime("%c"))

        with open(self.username + ".txt", "w", encoding="utf-8") as f:
            f.write(self.username + ' ' + base64.b64encode(enc_password).decode("utf-8"))

        print('You finished your registration')
        time.sleep(1.5)
        os.system("cls")
        self.mainpage()

    def mainpage(self):
        print('\tWelcome to the Task Tracking app,', self.username)
        print('=============================================')
        print('| " << "[1] ---> Your profile" << "         | ')
        print('| " << "[2] ---> View tasks"   << "         |')
        print('| " << "[3] ---> Create tasks" << "         | ')
        print('| " << "[4] ---> Edit tasks"   << "         | ')
        print('| " << "[5] ---> Delete tasks" << "         | ')
        print('| " << "[6] ---> exit" << "                 | ')
        print('=============================================\n')

        while self.page_choice != '6':
            self.page_choice = input('Enter the command -> ')
            self.commands_panel()

    def commands_panel(self):
        if self.page_choice == '0':
            os.system("cls")
            self.mainpage()

        elif self.page_choice == '1':
            os.system("cls")
            self.profile()
        
        elif self.page_choice == '2':
            os.system("cls")
            self.view_task()

        elif self.page_choice == '3':
            os.system("cls")
            self.create_task()
        
        elif self.page_choice == '4':
            os.system("cls")
            self.edit_task()

        elif self.page_choice == '5':
            os.system("cls")
            self.delete_task()

        elif self.page_choice == '6':
            os.system("cls")
            print('You have left the app. Thanks for using!')

        else:
            print('Command was not found')
            time.sleep(2)
            os.system("cls")
            self.mainpage()

    def profile(self):
        print('\tYour personal information: ')
        with open(self.username + "info.txt", "r", encoding="utf-8-sig") as f:
            for line in f:
                print(line.strip())

        choice = input('\nEnter <0> or any key to go back -> ')
        if choice == 0:
            os.system("cls")
            self.mainpage()
        
        else:
            os.system("cls")
            self.mainpage()

    def view_task(self):
        print('\tTask viewing page')
        print('Your current tasks: ')
        try:
            count = 1
            with open(self.username + "tasks.txt", "r", encoding="utf-8-sig") as f:
                for task in f:
                    print(count, '.',task.strip())
                    count += 1
            
            print('----------------------------')
            print('Operations :')
            choice = input('<0> -> Go back\n<1> -> Create tasks\n<2> -> Edit tasks\n<3> -> Delete tasks\nEnter your choice -> ')
            if choice == '0':
                os.system("cls")
                self.mainpage()
            
            elif choice == '1':
                os.system("cls")
                self.create_task()

            elif choice == '2':
                os.system("cls")
                self.edit_task()

            elif choice == '3':
                os.system("cls")
                self.delete_task()

            else:
                os.system("cls")
                print('Command was not found. For default keybinds we will take you back to the mainpage')
                time.sleep(2)
                os.system("cls")
                self.mainpage()

        except FileNotFoundError:
            print("You don't have task created before, or we did not found the file")
            choice = int(input('\nEnter <0> or any key to go back -> '))
            if choice == 0:
                os.system("cls")
                self.mainpage()

            else:
                os.system("cls")
                self.mainpage()

    def create_task(self):
        if os.path.exists(self.username + "tasks.txt"):
            print('We have found tasks saving file')

        else:
            print('Tasks saving file was not found, we will create a new one')

        time.sleep(2)
        while True:
            print('\tTask create page')
            name = input('Enter the task name (Enter <quit> to quit) -> ')
            if name == 'quit':
                break

            desc = input('Enter the descriptions for the task (Optional) -> ')
            if desc == '' or desc == 'none':
                desc = 'User has not provided descriptions'
            
            date = datetime.datetime.now()
            date = date.strftime("%c")

            try:
                with open(self.username + "tasks.txt", "a", encoding="utf-8") as f:
                    f.write('Task name: ' + name + ', Descriptions: ' + desc + ', Create date: ' + date + '\n')

            except FileNotFoundError:
                with open(self.username + "tasks.txt", "w", encoding="utf-8") as f:
                    f.write('Task name: ' + name + ', Descriptions: ' + desc + ', Create date: ' + date + '\n')
                
            print('Task saved')
            time.sleep(1.5)
            os.system("cls")
        
        print('You have quit tasks creation page')
        time.sleep(2)
        os.system("cls")
        self.mainpage()

    def edit_task(self):
        print('\tTask editing page')
        try:
            tasks = []
            with open(self.username + "tasks.txt", "r", encoding="utf-8-sig") as f:
                for task in f:
                    tasks.append(task.strip())

            while True:
                print('Here is your current tasks: ')
                count = 1
                for i in tasks:
                    print(count, '.', i)
                    count += 1

                choice = int(input('Enter the number for task to edit\n(ex: drink coffee is 3rd task, type <3>), enter <0> to quit -> '))
                if choice == 0:
                    break

                os.system("cls")
                name = input('Enter the task name ->')
                desc = input('Enter the descriptions for the task (Optional) -> ')
                if desc == '' or desc == 'none':
                    desc = 'User has not provided descriptions'
                
                date = datetime.datetime.now()
                date = date.strftime("%c")
                
                tasks[choice-1] = 'Task name: ' + name + ', Descriptions: ' + desc + ', Date edited: ' + date
                os.system("cls")
                print('Task has successfully edited')
                time.sleep(2)

            with open(self.username + "tasks.txt", "w", encoding="utf-8") as f:
                for line in tasks:
                    f.write(line + '\n')

            print('All progress saved')
            time.sleep(2)
            os.system("cls")
            self.mainpage()

        except FileNotFoundError:
            print("You don't have task created before, or we did not found the file")
            choice = input('\nEnter <0> or any key to go back -> ')
            if choice == 0:
                os.system("cls")
                self.mainpage()

            else:
                os.system("cls")
                self.mainpage()

    def delete_task(self):
        print('\tTask deleting page')
        try:
            tasks = []
            with open(self.username + "tasks.txt", "r", encoding="utf-8-sig") as f:
                for task in f:
                    tasks.append(task.strip())
            
            while True:
                print('Here is your current tasks: ')
                count = 1
                for i in tasks:
                    print(count, '.', i)
                    count += 1
            
                choice = int(input('Enter the lines for task to delete\n(Ex: Drink coffee is 3rd task, type <3>), Enter 0 to quit -> '))
                if choice == 0:
                    break

                tasks.pop(choice-1)
                os.system("cls")
                print('Task has successfully deleted')
                time.sleep(1.5)

            with open(self.username + "tasks.txt", "w", encoding="utf-8") as f:
                for line in tasks:
                    f.write(line + '\n')
            
            print('All progress saved')
            time.sleep(2)
            os.system("cls")
            self.mainpage()

        except FileNotFoundError:
            print("You don't have task created before, or we did not found the file")
            choice = input('\nEnter <0> or any key to go back -> ')
            if choice == 0:
                os.system("cls")
                self.mainpage()

            else:
                os.system("cls")
                self.mainpage()


def main():
    app = App()
    app.startup()


if __name__ == "__main__":
    main()

os.system("pause")