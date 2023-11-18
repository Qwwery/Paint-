import sys

from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QInputDialog, QApplication, QPushButton, QLabel


class LoginsErrorDialog(QDialog):
    def __init__(self, textError, cur):
        super().__init__()
        self.setWindowTitle(textError)
        self.setGeometry(700, 250, 300, 200)

        self.cur = cur

        label = QLabel(textError, self)
        label.move(120, 100)


        self.resize(300, 200)


        oklButton = QPushButton('ok', self)
        oklButton.move(10, 10)
        oklButton.resize(80, 30)
        oklButton.clicked.connect(self.ok)

        cancelButton = QPushButton('cancel', self)
        cancelButton.move(100, 10)
        cancelButton.resize(80, 30)
        cancelButton.clicked.connect(self.cancel)

        createButton = QPushButton('create', self)
        createButton.move(190, 10)
        createButton.resize(80, 30)
        createButton.clicked.connect(self.create)

        print('test 1')

    def ok(self):
        print('test 2')
        self.close()

    def cancel(self):
        print('test 2')

    def create(self):
        print('test 2')
        login = QInputDialog.getText('Создание аккаунта', 'Введите логин:')
        if login in self.cur.execute('SELECT Login FROM Users').fetchall():
            error = LoginsErrorDialog('Такой логин уже существует', self.cur)
        else:
            password = QInputDialog.getText('Создание аккаунта', 'Введите пароль:')
            self.cur.execute(f'INSERT INTO Users(login, Password) VALUES({login}, {password})')
    print('test 2')
