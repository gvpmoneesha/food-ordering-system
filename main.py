from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sys
import sqlite3
import bcrypt

con = sqlite3.connect('food.db')
cursor=con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
               username TEXT NOT NULL,
               email TEXT NOT NULL,
               password TEXT NOT NULL,
               comPassword TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants(
               id TEXT NOT NULL,
               name TEXT NOT NULL PRIMARY KEY,
               address TEXT NOT NULL,
               phone TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu(
               id TEXT NOT NULL,
               name TEXTEGER NOT NULL,
               price INT NOT NULL,
               restaurant_name TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart(
               number INTEGER PRIMARY KEY AUTOINCREMENT,
               userName TEXT NOT NULL,
               resName TEXT NOT NULL,
               itemName TEXT NOT NULL,
               quantity INTEGER NOT NULL,
               id TEXT NOT NULL,
               status TEXT NOT NULL,
               price INTEGER NOT NULL,
               total INTEGER NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS managers(
               username TEXT NOT NULL,
               email TEXT NOT NULL,
               password TEXT NOT NULL,
               comPassword TEXT NOT NULL)''')

user = ''

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("login.ui",self) 

 
        self.pushButton_2.clicked.connect(self.signUp2)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.manager)

    def signUp2(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.hide()
        signUp_ui.show()

    def manager(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.hide()
        managerLogin_ui.show()

    def login(self):
        global user
        user = username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username != '' and password != '':
            cursor.execute('SELECT password FROM users WHERE username=?',[username])
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                    QMessageBox.information(None,"Message","Your logging is success.")
                    self.hide()
                    main_ui.show()
                else:
                    QMessageBox.information(None,"Message","Invalid Username or Password.")
            else:
                QMessageBox.information(None,"Message","Invalid Username or Password.")
        else:
            QMessageBox.information(None,"Message","All data required.")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

class signUp(QMainWindow):
    def __init__(self):
        super(signUp,self).__init__()
        uic.loadUi("signUp.ui",self)  

        self.pushButton.clicked.connect(self.signUp1)
        self.pushButton_2.clicked.connect(self.login2)

    def login2(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.hide()
        login_ui.show() 
        

    def signUp1(self):
        username = self.lineEdit.text()
        email = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        comPassword = self.lineEdit_4.text()

        if password == comPassword:

            if username != '' and email != '' and password != '' and comPassword != '':
                cursor.execute('SELECT username FROM users WHERE username=?',[username])
                if cursor.fetchone() is not None:
                    QMessageBox.information(None,"Message","User name is already exists.")
                else:
                    encodePassword = password.encode('utf-8')
                    hashedPassword = bcrypt.hashpw(encodePassword,bcrypt.gensalt())
                    encodePassword1 = comPassword.encode('utf-8')
                    hashedPassword1 = bcrypt.hashpw(encodePassword1,bcrypt.gensalt())
                    cursor.execute('INSERT INTO users VALUES (?,?,?,?)',[username,email,hashedPassword,hashedPassword1])
                    con.commit()
                    QMessageBox.information(None,"Message","Data insert is success.")
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.hide()
                    login_ui.show()
            else:
                QMessageBox.information(None,"Message","All fields are required.")

        else:
            QMessageBox.information(None,"Message","Please check the password.")

class main(QMainWindow):
    def __init__(self):
        super(main,self).__init__()
        uic.loadUi("main.ui",self)  

        self.pushButton_3.clicked.connect(self.cart1)
        self.pushButton_4.clicked.connect(self.viewCart)
        self.pushButton_5.clicked.connect(self.track)
        self.pushButton_7.clicked.connect(self.exit)

    def cart1(self):
        self.hide()
        cart_ui.show()

    def viewCart(self):
        self.hide()
        viewCart_ui.show()

    def track(self):
        self.hide()
        track_ui.show()

    def exit(self):
        self.hide()
        login_ui.show()

class restaurant(QMainWindow):
    def __init__(self):
        super(restaurant,self).__init__()
        uic.loadUi("restaurant.ui",self) 

        self.pushButton_2.clicked.connect(self.add)
        self.pushButton_5.clicked.connect(self.main1)
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4.clicked.connect(self.display)
        self.pushButton.clicked.connect(self.menu1)

    def main1(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        managerMain_ui.show()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")

    def menu1(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        menu_ui.show()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")

    def add(self):
        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        address = self.lineEdit_3.text()
        phone = self.lineEdit_4.text()

        if id != '' and name != '' and address != '' and phone != '':
            cursor.execute('SELECT name FROM restaurants WHERE name=?',[name])
            result = cursor.fetchone()
            cursor.execute('SELECT id FROM restaurants WHERE id=?',[id])
            result1 = cursor.fetchone()
            if not result1:
                if not result:
                    cursor.execute('INSERT INTO restaurants VALUES (?,?,?,?)',[id,name,address,phone])
                    con.commit()
                    QMessageBox.information(None,"Message","Data insert is success.")
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                else:
                    QMessageBox.information(None,"Message","The restaurant is exists.")
            else:
                QMessageBox.information(None,"Message","This restaurant id is exists.")
        else:
            QMessageBox.information(None,"Message","Please enter the field.")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        

    def delete(self):
        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        
        if id != '':
            cursor.execute('SELECT * FROM restaurants WHERE name=?',[name])
            result1 = cursor.fetchone()
            if result1:
                cursor.execute('DELETE FROM restaurants WHERE name=?',[name])
                cursor.execute('DELETE FROM menu WHERE restaurant_name=?', [name])
                con.commit()
                QMessageBox.information(None,"Message","Restaurant delete is success.")
            else:
                QMessageBox.information(None,"Message","Restaurant field is empty or this restaurant is not exist.")
        else:
            QMessageBox.information(None,"Message","Id field is can\'t empty.")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
            
    def display(self):
        cursor.execute('SELECT * FROM restaurants')
        con.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Restaurant_No','Name','Address','Phone_Number']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                restaurant = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j,restaurant)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")

class menu(QMainWindow):
        def __init__(self):
            super(menu,self).__init__()
            uic.loadUi("menu.ui",self)  
            self.restaurant()

            self.pushButton.clicked.connect(self.add1)
            self.pushButton_2.clicked.connect(self.delete1)
            self.pushButton_3.clicked.connect(self.display1)
            self.pushButton_4.clicked.connect(self.back_restaurant)
            self.pushButton_5.clicked.connect(self.restaurant)

        def restaurant(self):
            self.comboBox.clear()
            cursor.execute('SELECT name FROM restaurants')
            result = cursor.fetchall()
            for item in result:
                self.comboBox.addItem(item[0])

        def add1(self):
            id = self.lineEdit.text()
            name = self.lineEdit_2.text()
            iPrice = self.lineEdit_3.text()
            resName = self.comboBox.currentText()
            #print(id,name,iPrice,resName)

            if id != '' and name != '' and iPrice != '' and resName != '':
                price = int(iPrice)
                cursor.execute('SELECT id FROM menu WHERE id=? AND restaurant_name=?',[id,resName])
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO menu VALUES (?,?,?,?)',[id,name,price,resName])
                    con.commit()
                    QMessageBox.information(None,"Message","Data insert is success.")
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.lineEdit_3.setText("")
                    self.comboBox.setCurrentIndex(-1)
                else:
                    QMessageBox.information(None,"Message","This item number is exist.")
            else:
                QMessageBox.information(None,"Message","Please enter the field.")

        def delete1(self):
            id = self.lineEdit.text()
            resName = self.comboBox.currentText()
        
            if id != '' and resName != '':
                cursor.execute('SELECT * FROM menu WHERE id=?',[id])
                result2 = cursor.fetchone()
                if result2:
                    cursor.execute('DELETE FROM menu WHERE id=? and  restaurant_name=?',[id,resName])
                    con.commit()
                    QMessageBox.information(None,"Message","Item delete is success.")
                else:
                    QMessageBox.information(None,"Message","Item is not found.")
            else:
                QMessageBox.information(None,"Message","Id field and restaurant name fields are can\'t empty.")

        def display1(self):
            cursor.execute('SELECT * FROM menu')
            con.commit()
            rows = cursor.fetchall()
            self.tableWidget.setRowCount(len(rows))
            column_names = ['Item_No','Name','Price','Restaurant_Name']
            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(i,j,item)

        def back_restaurant(self):
            self.tableWidget.setRowCount(0)
            self.hide()
            restaurant_ui.show()

class cart(QMainWindow):
    def __init__(self):
            super(cart,self).__init__()
            uic.loadUi("cart.ui",self) 
            self.comboBox.currentIndexChanged.connect(self.item2)
            self.pushButton.clicked.connect(self.cart1)
            self.pushButton_2.clicked.connect(self.restaurant3)
            self.pushButton_3.clicked.connect(self.back2)

    def back2(self):
        self.hide()
        main_ui.show()
        self.lineEdit.setText('')
        
    def restaurant3(self):
            self.comboBox.clear()
            self.comboBox_2.clear()
            cursor.execute('SELECT name FROM restaurants')
            result = cursor.fetchall()
            for item in result:
                self.comboBox.addItem(item[0])
            self.item2()

    def item2(self):
            rName = self.comboBox.currentText()
            if rName != '':
                self.comboBox_2.clear()
                cursor.execute('SELECT id,name,price FROM menu WHERE restaurant_name=?',[rName])
                result1 = cursor.fetchall()
                for item in result1:
                    id,name,price = item
                    self.comboBox_2.addItem(f"{id} - {name} - Rs.{price}")
            else:
                    QMessageBox.information(None,"Message","Restaurant field is empty.")
            
    def cart1(self):
        rName1 = self.comboBox.currentText()
        if rName1 !='':
            rName1 = self.comboBox.currentText()
            iName = self.comboBox_2.currentText().split(' ')[2]
            quantity = self.lineEdit.text()
            id = self.comboBox.currentText().split(' ')[0]
            price = int(self.comboBox_2.currentText().split('.')[1])
            status = 'cart'
            total = 0
        
            if rName1 != '' and iName != '' and quantity != '' and quantity !='':
                quantity1 = int(quantity)
                total = price * quantity1
                cursor.execute('INSERT INTO cart (userName,resName,itemName,quantity,id,status,price,total) VALUES (?,?,?,?,?,?,?,?)',[user,rName1,iName,quantity1,id,status,price,total])
                con.commit()
                QMessageBox.information(None,"Message","Items are added to the cart.")
            else:
                QMessageBox.information(None,"Message","Quantity field is empty.")
            self.lineEdit.setText('')
        else:
            QMessageBox.information(None,"Message","Click the load restaurant button.")

class viewCart(QMainWindow):
    def __init__(self):
            super(viewCart,self).__init__()
            uic.loadUi("viewCart.ui",self) 

            self.pushButton_2.clicked.connect(self.main3)
            self.pushButton.clicked.connect(self.display)
            self.pushButton_3.clicked.connect(self.delete)
            self.pushButton_4.clicked.connect(self.buy)

    def main3(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        main_ui.show()
        self.lineEdit.setText('')

    def display(self):
        total = 0
        cursor.execute("SELECT number,userName,resName,itemName,quantity,total FROM cart WHERE status='cart'")
        con.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Number','User Name','Restaurant Name','Item Name','Quantity','total']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                displayCart = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j,displayCart)
                if j==5:
                    total = total + value 
        self.label_4.setText("Charge = RS." + str(total))  
        self.lineEdit.setText('') 

    def delete(self):
        number1 = self.lineEdit.text()
        if number1 != '':
            number2 = int(number1)
            cursor.execute('SELECT number FROM cart WHERE number=?',[number2])
            if cursor.fetchone() is not None:
                cursor.execute("DELETE FROM cart WHERE number = ?", [number2])
                con.commit()
                QMessageBox.information(None,"Message","Data delete is success.")
                self.display()
            else:
                QMessageBox.information(None,"Message","This number is can\'t find.")
        else:
            QMessageBox.information(None,"Message","Number field is empty.")
        self.lineEdit.setText('')

    def buy(self):
        charge = int(self.label_4.text().split('.')[1])
        if charge > 0:
            cursor.execute("UPDATE cart SET status ='confirmed' WHERE userName = ? AND status ='cart'", [user])
            con.commit()
            self.display()
        else:
            QMessageBox.information(None,"Message","Add to item for cart on display the cart item.")
        self.lineEdit.setText('')

class track(QMainWindow):
    def __init__(self):
            super(track,self).__init__()
            uic.loadUi("tracking.ui",self) 

            self.pushButton.clicked.connect(self.main4)
            self.pushButton_2.clicked.connect(self.display)

    def main4(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        main_ui.show()

    def display(self):
        cursor.execute("SELECT number,userName,resName,itemName,quantity,total,status FROM cart WHERE status!='cart' and userName=?",[user])
        con.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Number','User Name','Restaurant Name','Item Name','Quantity','total','Status']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                tracking = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j,tracking)

class manage(QMainWindow):
    def __init__(self):
            super(manage,self).__init__()
            uic.loadUi("manageTracking.ui",self)

            self.pushButton.clicked.connect(self.back5)
            self.pushButton_2.clicked.connect(self.display)
            self.pushButton_3.clicked.connect(self.update)

    def back5(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        managerMain_ui.show()
        self.lineEdit.setText("")

    def display(self):
        cursor.execute("SELECT number,userName,resName,itemName,quantity,total,status FROM cart WHERE status!='cart'")
        con.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Number','User Name','Restaurant Name','Item Name','Quantity','total','Status']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                managing = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j,managing)
        self.lineEdit.setText("")

    def update(self):
        number = self.lineEdit.text()
        status = self.comboBox.currentText()

        if number != '' and status != '':
            cursor.execute('UPDATE cart SET status=? WHERE number=?', [status, number])
            con.commit()
            self.display()
            QMessageBox.information(None,"Message","Status update is success.")
        else:
            QMessageBox.information(None,"Message","Fields are empty.")
        self.lineEdit.setText("")

class ManagerLogin(QMainWindow):
    def __init__(self):
        super(ManagerLogin, self).__init__()
        uic.loadUi("managerLogin.ui",self)

        self.pushButton_2.clicked.connect(self.signUp)
        self.pushButton_3.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.login)

    def signUp(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.hide()
        managerSignUp_ui.show()

    def back(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.hide()
        login_ui.show()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username != '' and password != '':
            cursor.execute('SELECT password FROM managers WHERE username=?',[username])
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                    QMessageBox.information(None,"Message","Your logging is success.")
                    self.hide()
                    managerMain_ui.show()
                else:
                    QMessageBox.information(None,"Message","Invalid Username or Password.")
            else:
                QMessageBox.information(None,"Message","Invalid Username or Password.")
        else:
            QMessageBox.information(None,"Message","All data required.")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

class ManagerSignUp(QMainWindow):
    def __init__(self):
        super(ManagerSignUp,self).__init__()
        uic.loadUi("managerSignUp.ui",self)  

        self.pushButton.clicked.connect(self.signUp1)
        self.pushButton_2.clicked.connect(self.login2)

    def login2(self):
        self.hide()
        managerLogin_ui.show() 
        

    def signUp1(self):
        username = self.lineEdit.text()
        email = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        comPassword = self.lineEdit_4.text()

        if password == comPassword:

            if username != '' and email != '' and password != '' and comPassword != '':
                cursor.execute('SELECT username FROM managers WHERE username=?',[username])
                if cursor.fetchone() is not None:
                    QMessageBox.information(None,"Message","User name is already exists.")
                else:
                    encodePassword = password.encode('utf-8')
                    hashedPassword = bcrypt.hashpw(encodePassword,bcrypt.gensalt())
                    encodePassword1 = comPassword.encode('utf-8')
                    hashedPassword1 = bcrypt.hashpw(encodePassword1,bcrypt.gensalt())
                    cursor.execute('INSERT INTO managers VALUES (?,?,?,?)',[username,email,hashedPassword,hashedPassword1])
                    con.commit()
                    QMessageBox.information(None,"Message","Data insert is success.")
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.hide()
                    managerLogin_ui.show()
            else:
                QMessageBox.information(None,"Message","All fields are required.")

        else:
            QMessageBox.information(None,"Message","Please check the password.")

class ManagerMain(QMainWindow):
    def __init__(self):
        super(ManagerMain,self).__init__()
        uic.loadUi("managerMain.ui",self)  

        self.pushButton.clicked.connect(self.restaurant1)
        self.pushButton_6.clicked.connect(self.manage)
        self.pushButton_7.clicked.connect(self.exit)

    def restaurant1(self):
        self.hide()
        restaurant_ui.show()

    def manage(self):
        self.hide()
        manage_ui.show()

    def exit(self):
        self.hide()
        managerLogin_ui.show()


app = QApplication(sys.argv)
login_ui = Login()
signUp_ui = signUp()
main_ui = main()
restaurant_ui = restaurant()
menu_ui = menu()
cart_ui = cart()
viewCart_ui = viewCart()
track_ui = track()
manage_ui = manage()
managerLogin_ui =ManagerLogin()
managerSignUp_ui = ManagerSignUp()
managerMain_ui = ManagerMain()


login_ui.show()
sys.exit(app.exec_())