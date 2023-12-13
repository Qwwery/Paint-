from django.shortcuts import render, redirect
from .forms import ProfilsForm, EnterProfilForm, ImageForm
from .models import Profils
import sqlite3
from django.http import HttpResponse
from datetime import datetime
from base64 import  b64decode


def account(request):
    return render(request, 'main/account.html')


def main(request):
    return render(request, 'main/viewing.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def about(request):
    return render(request, 'main/about.html')


def create(request):
    form = ProfilsForm()
    cor = sqlite3.connect('db.sqlite3')
    cur = cor.cursor()
    error = ''
    if request.method == 'POST':
        form = ProfilsForm(request.POST)
        login = str(form['login'].value())
        password = str(form['password'].value())
        if login in [i[0] for i in cur.execute('select login from main_profils').fetchall()]:
            error = 'данный логин уже используется'
        elif form.is_valid():
            cor_2 = sqlite3.connect('../../../База данных/profils.db')
            cur_2 = cor_2.cursor()

            cur_2.execute(f'Insert Into Users(login, password) VALUES("{login}", "{password}")')
            cor_2.commit()

            form.save()
            with open('this login and password.txt', 'w') as this_login:
                this_login.write(f'{login}\n{password}')
            return redirect('main')
        else:
            error = 'Не все поля заполненны корректно!'

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'main/create.html', data)


def enter(request):
    form = EnterProfilForm()
    cor = sqlite3.connect('db.sqlite3')
    cur = cor.cursor()
    error = ''

    open('this login and password.txt', 'w').close()

    if request.method == 'POST':
        form = ProfilsForm(request.POST)
        login = str(form['login'].value())
        password = str(form['password'].value())
        if login not in [i[0] for i in cur.execute('select login from main_profils').fetchall()]:
            error = 'Неверный логин!'
        elif form.is_valid():
            if password != [i[0] for i in cur.execute('select password from main_profils').fetchall()][0]:
                error = 'Неверный пароль!'
            else:
                with open('this login and password.txt', 'w') as this_login:
                    this_login.write(f'{login}\n{password}')
                return redirect('main')
        else:
            error = 'Не все поля заполненны корректно!'

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'main/account.html', data)


def viewing(request):
    tekst = ''
    with open('this login and password.txt', 'r') as this_login:
        this_login = this_login.read()
        if this_login != '':
            tekst = f'Привет, {this_login.split()[0]}!'
            link = 'main/home'
        else:
            tekst = 'Нет аккаунта?'
            link = 'main/create'

    all_data = []
    check = []
    photo = []

    with open('this login and password.txt', 'r') as this_login:
        this_login = this_login.read()
        with open('info.txt', 'r') as f:
            info = f.read().split('\n')
            for i in range(len(info)):
                if info[i] != '':
                    all_data.append(info[i].split('_'))
                    photo.append(info[i].split('_')[-1])
                    check.append({'login': info[i].split('_')[0],
                                  'name': info[i].split('_')[1],
                                  'dateandtime': info[i].split('_')[2],
                                  'data': info[i].split('_')[-1]})
    data = {
        'tekst': tekst,
        'link': link,
        'data': all_data,
        'photo': photo,
        'check': check
    }

    return render(request, 'main/viewing.html', data)


def home(request):
    return render(request, 'main/home.html')

def new(request):
    form = ImageForm()
    cor = sqlite3.connect('db.sqlite3')
    cur = cor.cursor()

    cor_2 = sqlite3.connect('../../../База данных/profils.db')
    cur_2 = cor_2.cursor()

    error = ''
    if request.method == 'POST':
        form = ImageForm(request.POST)
        with open('this login and password.txt', 'r') as this_login:
            this_login = this_login.read()
            try:
                if this_login == '':
                    error = 'Войдите в аккаунт прежде чем выкладывать фото!'
                else:
                    name = form['name'].value()
                    if len(cur_2.execute(f'select name from base64photo').fetchall()) == 0:
                        error = 'У вас нет рисунков! Создайте их в приложении, по ссылке ниже.'
                    elif name not in [i[0].split('.')[0] for i in cur_2.execute(f'select Name from Base64Photo where Login = "{this_login.split()[0]}"').fetchall()]:
                        error = 'Вы не можете выкладывать рисунки, созданные не вами!'
                    else:
                        cur.execute(f'Insert Into main_image(Login, name) VALUES("{this_login.split()[0]}", "{name}")')
                        cor.commit()
                        with open('info.txt', 'a') as f:
                            data = str(cur_2.execute(f'Select Base64Photo From Base64Photo '
                                            f'Where Login = "{this_login.split()[0]}" AND'
                                            f' Name = "{name}.png"').fetchall()[-1][-1]).split("'")[1]
                            f.write(f'{name}_{this_login.split()[0]}_{str(datetime.now()).split(".")[0]}_{data}')
                            f.write('\n')
                        return redirect('main')

            except Exception:
                error = 'Ошибка! Попробуйте перезагрузить страницу или выложить изображение позже!'

    data = {
        'error': error,
        'form': form
    }

    return render(request, 'main/new.html', data)

