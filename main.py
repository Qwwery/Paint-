import os.path
import sqlite3
import sys
from base64 import b64encode, b64decode

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QColorDialog, QPushButton
from PyQt5.QtWidgets import QLabel, QInputDialog, QSlider, QUndoCommand, QUndoStack, QFileDialog
from PyQt5.QtWidgets import QMessageBox
import webbrowser

class LoginsErrorDialog(QMainWindow):
    def __init__(self, textError, cur, cor):
        super().__init__()
        self.setWindowTitle(textError)
        self.setGeometry(760, 290, 280, 180)

        self.cur = cur
        self.cor = cor

        label = QLabel(textError, self)
        label.move(60, 50)

        self.initUi()

    def initUi(self):
        oklButton = QPushButton('ok', self)
        oklButton.move(90, 150)
        oklButton.resize(50, 25)
        oklButton.clicked.connect(self.ok)

        cancelButton = QPushButton('cancel', self)
        cancelButton.move(140, 150)
        cancelButton.resize(50, 25)
        cancelButton.clicked.connect(self.cancel)

        createButton = QPushButton('create', self)
        createButton.move(190, 150)
        createButton.resize(50, 25)
        createButton.clicked.connect(self.create)

    def ok(self):
        self.close()

    def cancel(self):
        self.close()

    def create(self):
        login = QInputDialog.getText(self, 'Создание аккаунта.', 'Введите логин:')
        if login in self.cur.execute('SELECT Login FROM Users').fetchall():
            error = LoginsErrorDialog('Такой логин уже существует', self.cur)
        else:
            password = QInputDialog.getText(self, 'Создание аккаунта', 'Введите пароль:')
            self.cur.execute(f'INSERT INTO Users(login, Password) VALUES("{login[0]}", "{password[0]}")')
            self.cor.commit()

            cor = sqlite3.connect('Сервер/Jango lesons/paint/db.sqlite3')
            cur = cor.cursor()

            cur.execute(f'Insert Into main_profils(login, password) VALUES("{login}", "{password}")')
            cor.commit()

            os.chdir('База данных/Фото/')
            os.mkdir(login[0])
        self.close()


class UndoCommand(QUndoCommand):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mPrevImage = parent.image.copy()
        self.mCurrImage = parent.image.copy()

    def undo(self):
        self.mCurrImage = self.parent.image.copy()
        self.parent.image = self.mPrevImage
        self.parent.update()

    def redo(self):
        self.parent.image = self.mCurrImage
        self.parent.update()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        TOP = 400
        LEFT = 200
        WIDTH = 1000
        HEIGHT = 800

        icon = 'icon/plex-sai-icon-png-icon.jpg'

        self.setWindowTitle('Paint++')
        self.setGeometry(TOP, LEFT, WIDTH, HEIGHT)
        self.setWindowIcon(QIcon(icon))
        self.InitUi()

    def InitUi(self):
        self.label = QLabel(self)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        Sayt = mainMenu.addMenu('Сайт')

        saytAsAction = QAction('Посетить сайт', self)
        Sayt.addAction(saytAsAction)
        saytAsAction.triggered.connect(lambda: webbrowser.open('http://127.0.0.1:8000/main'))

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.cor = sqlite3.connect('База данных/profils.db')
        self.cur = self.cor.cursor()

        saveAsAction = QAction(QIcon('icon/2023-10-07_13-22-51.png'), 'Сохранить как', self)
        saveAsAction.setShortcut('Ctrl+S')
        fileMenu.addAction(saveAsAction)
        saveAsAction.triggered.connect(self.save_as)

        saveAction = QAction(QIcon('icon/2023-10-07_13-26-57.png'), 'Сохранить', self)
        saveAction.setShortcut('Ctrl+P')
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        openAction = QAction(QIcon('icon/2023-10-07_13-26-57.png'), 'Открыть', self)
        openAction.setShortcut('Ctrl+O')
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        self.colorButton = QPushButton(self)
        self.colorButton.move(700, 20)
        self.colorButton.setText("Выбрать цвет")
        fileMenu.addAction(openAction)
        self.colorButton.clicked.connect(self.set_color)

        self.clearButton = QPushButton(self)
        self.clearButton.move(0, 20)
        self.clearButton.setText('Очистить')
        self.clearButton.clicked.connect(self.clear)

        self.sizeSlider = QSlider(Qt.Horizontal, self)
        self.sizeSlider.move(120, 20)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(25)
        self.sizeSlider.setValue(2)
        self.sizeSlider.valueChanged[int].connect(self.set_size)

        self.sizeLabel = QLabel(self)
        self.sizeLabel.move(225, 20)
        self.sizeLabel.setText('2')

        self.eraserButton = QPushButton(self)
        self.eraserButton.move(0, 50)
        self.eraserButton.setText('Ластик')
        self.eraserButton.clicked.connect(self.eraser)

        self.squareButton = QPushButton(self)
        self.squareButton.setIcon(QIcon('icon/db12cd5416b80f34701a0834bfe8671f.png'))
        self.squareButton.resize(20, 20)
        self.squareButton.move(250, 20)
        self.squareButton.clicked.connect(self.square)

        self.triangleButton = QPushButton(self)
        self.triangleButton.setIcon(QIcon('icon/1614572172_39-p-treugolnik-na-belom-fone-43.jpg'))
        self.triangleButton.resize(20, 20)
        self.triangleButton.move(270, 20)
        self.triangleButton.clicked.connect(self.triangle)

        self.elipsButton = QPushButton(self)
        self.elipsButton.setIcon(QIcon(
            'icon/png-transparent-black-circle-computer-icons-connections-monochrome-black-desktop-wallpaper.png'))
        self.elipsButton.resize(20, 20)
        self.elipsButton.move(290, 20)
        self.elipsButton.clicked.connect(self.elips)

        self.penButton = QPushButton(self)
        self.penButton.setIcon(
            QIcon('icon/brush-icon-on-white-background-black-brush-sign-paint-symbol-flat-style-vector.jpg'))
        self.penButton.resize(20, 20)
        self.penButton.move(310, 20)
        self.penButton.clicked.connect(self.pen)

        self.square_flag = False
        self.triangle_flag = False
        self.elips_flag = False

        self.do_paint = False
        self.color = QColor(0, 0, 0)

        self.pos_1, self.pos_2 = 0, 0

        self.size_painter = 4

        self.mUndoStack = QUndoStack(self)
        self.mUndoStack.setUndoLimit(20)

        self.mUndoStack.canUndoChanged.connect(self.can_undo_changed)
        self.mUndoStack.canRedoChanged.connect(self.can_redo_changed)

        self.actionUndo = self.menuBar().addAction("<")
        self.actionUndo.triggered.connect(self.mUndoStack.undo)
        self.actionRedo = self.menuBar().addAction(">")
        self.actionRedo.triggered.connect(self.mUndoStack.redo)

        self.can_undo_changed(self.mUndoStack.canUndo())
        self.can_redo_changed(self.mUndoStack.canRedo())

        self.start_pos = None
        self.last_pos = None
        self.is_pressed = False

    def set_color(self):
        self.color = QColorDialog.getColor()

        self.do_paint = True
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_pos = event.pos()

        self.is_pressed = True
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            if not (self.square_flag or self.elips_flag):
                canvasPainter = QPainter(self.image)
                canvasPainter.setPen(QPen(self.color, self.size_painter, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                canvasPainter.drawLine(self.last_pos, event.pos())
            self.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.make_undo_command()
        self.draw(self.image)

        self.is_pressed = False
        self.last = event.pos()
        if event.button == Qt.LeftButton:
            self.drawing = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.image.rect(), self.image)
        if self.is_pressed:
            self.draw(self)

    def draw(self, parent):
        painter = QPainter(parent)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        rect = QRect(self.start_pos, self.last_pos)
        painter.setPen(Qt.NoPen)
        painter.setPen(QPen(self.color, self.size_painter, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.square_flag:
            painter.drawRect(rect)
        elif self.elips_flag:
            painter.drawEllipse(rect)
        elif self.triangle_flag:
            pass

    def save_as(self):
        login, isLong = QInputDialog.getText(self, 'Ввойдите в аккаунт.', 'Логин:')
        if isLong and login in [i[0] for i in self.cur.execute('SELECT Login FROM Users').fetchall()]:
            password, isPasswordLong = QInputDialog.getText(self, 'Введите пароль.', 'Пароль:')

            if password in [i[0] for i in
                            self.cur.execute(f'SELECT Password FROM Users Where "{login}" = login').fetchall()]:
                name, isNameLong = QInputDialog.getText(self, '', 'Название рисунка')
                if isNameLong and name in [i[0].split('.')[0] for i in self.cur.execute(
                        f'SELECT Name FROM Base64Photo Where Login = "{login}"').fetchall()]:

                    country = QMessageBox.question(self, 'Внимание!',
                                                   'Вы уже использовали данное имя для рисунка.')
                elif isNameLong:
                    self.image.save('База данных/Фото/Архив/' + login + name + '.png')
                    with open('База данных/Фото/Архив/' + login + name + '.png', 'rb') as image:
                        binary = b64encode(image.read())
                        self.cur.execute(f'Insert Into Base64Photo(Login, Base64Photo, Name, Reactions) Values("{login}", "{binary}", "{name}.png", 0)')
                        self.cor.commit()
                        self.image.save('База данных/Фото/' + login + '/' + name + '.png')
            elif isPasswordLong:
                country = QMessageBox.question(self, 'Внимание!',
                                               'Вы ввели не верный пароль.')
        elif isLong:
            self.showDialog('Такого логина нет')

    def open(self):
        login, isLong = QInputDialog.getText(self, 'Ввойдите в аккаунт.', 'Логин:')
        if isLong and login in [i[0] for i in self.cur.execute('SELECT Login FROM Users').fetchall()]:
            password, isPasswordLong = QInputDialog.getText(self, 'Введите пароль.', 'Пароль:')
            if isPasswordLong and password in [i[0] for i in
                                               self.cur.execute(
                                                   f'SELECT Password FROM Users Where "{login}" = login').fetchall()]:

                self.pathPhoto = QFileDialog.getOpenFileName(self, 'Выбирите изображение', '',
                                                             'Картинка (*.png)')[0].split('/')
                self.fname = self.pathPhoto[-1]
                try:
                    data = self.cur.execute(f'Select Base64Photo From Base64Photo '
                                            f'Where Login = "{login}" AND'
                                            f' Name = "{self.fname}"').fetchall()[-1][-1]
                    data = str(data).split("'")[1]
                    if self.fname in [i[0] for i in self.cur.execute(
                            f'Select Name From Base64Photo Where Login = "{login}"').fetchall()]:
                        with open(f'База данных/фото/Архив/{login}{self.fname}', 'wb') as f:
                            f.write(b64decode(data))
                        self.image = QImage(f'База данных/фото/Архив/{login}{self.fname}')
                    else:
                        country = QMessageBox.question(self, 'Внимание!',
                                                       'Вы не можете открыть не ваши фото.')
                except Exception:
                    country = QMessageBox.question(self, 'Внимание!',
                                                   'Вы не можете открыть не ваши фото.')

            elif isPasswordLong:
                country = QMessageBox.question(self, 'Внимание!',
                                               'Вы ввели не верный пароль.')
        elif isLong:
            country = QMessageBox.question(self, 'Внимание!',
                                           'Вы ввели не верный логин.')


    def save(self):
        try:
            login, isLong = QInputDialog.getText(self, 'Ввойдите в аккаунт.', 'Логин:')
            if isLong and login in [i[0] for i in self.cur.execute('SELECT Login FROM Users').fetchall()]:
                if self.fname in self.cur.execute('Select Name From Base64Photo Where Login = {}'.format(login)):
                    password, isPasswordLong = QInputDialog.getText(self, 'Введите пароль.', 'Пароль:')
                    if isPasswordLong and password in [i[0] for i in
                                                       self.cur.execute(
                                                           f'SELECT Password FROM Users Where "{login}" = login').fetchall()]:
                        self.image.save('База данных/Фото/{}/'.format(login))
                    elif isPasswordLong:
                        country = QMessageBox.question(self, 'Внимание!',
                                                       'Вы ввели не верный логин.')
                else:
                    country = QMessageBox.question(self, 'Внимание!',
                                                   'Вы не можете пересохранить новый рисунок.')
            elif isLong:
                country = QMessageBox.question(self, 'Внимание!',
                                               'Вы ввели не верный логин.')
        except AttributeError:
            country = QMessageBox.question(self, 'Внимание!',
                                           'Вы не можете пересохранить новый рисунок.')


        # self.cur.execute('Update Base64Photo From B')

    def clear(self):
        country = QMessageBox.question(self, 'Вы точно хотите очистить экран?',
                                       'Все несохраненые элементы будут удалены.')
        if country == 16384:
            self.image.fill(Qt.white)

    def set_size(self, value):
        self.sizeLabel.setText(str(value))
        self.size_painter = value

    def eraser(self):
        self.color = QColor(255, 255, 255)

        self.square_flag = False
        self.triangle_flag = False
        self.elips_flag = False
        self.is_pen = True

    def square(self):
        self.square_flag = True
        self.elips_flag = False
        self.is_pen = False
        self.triangle_flag = False

    def triangle(self):
        self.triangle_flag = True
        self.square_flag = False
        self.is_pen = False
        self.elips_flag = False

    def elips(self):
        self.elips_flag = True
        self.square_flag = False
        self.is_pen = False
        self.triangle_flag = False

    def pen(self):
        self.is_pen = True
        self.elips_flag = False
        self.square_flag = False
        self.triangle_flag = False

    def can_undo_changed(self, enabled):
        self.actionUndo.setEnabled(enabled)

    def can_redo_changed(self, enabled):
        self.actionRedo.setEnabled(enabled)

    def make_undo_command(self):
        self.mUndoStack.push(UndoCommand(self))

    def showDialog(self, text=''):
        self.dialog = LoginsErrorDialog(text, self.cur, self.cor)
        self.dialog.show()

    # -------------------------------


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec())
