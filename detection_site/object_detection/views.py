from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from datetime import time, datetime

from django.contrib import messages



# Create your views here.
def home(request):
    doctors = Doctors.objects.all() # Берем список докторов для показа на главной странице
    name = request.session.get('name')  # Получаем имя из сессии для показа нужной главнй страницы
    context = {
        'name': name,
        'doctors': doctors,
    } # передаем докторов и имя по
    return render(request, 'home.html', context=context)

# Функция для смены url
def home_log(request):
    doctors = Doctors.objects.all()
    name = request.session.get('name')  # Получаем имя из сессии
    context = {
        'name': name,
        'doctors': doctors,
    }
    return render(request, 'home.html', context=context)

# функция для входа в систему
def login(request):
    request.session['name'] = ' ' # обнуляем сессию, т.к. в аккаунт входа не выполнено
    info = {
        'error': '',
        'name': '',
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password') # Пост запросы на логин и пароль для будущей проверки в бд

        try:
            # берем имена зарегестрированных пользователей
            user = Users.objects.get(name=name)

            # проверка пароля
            if user.password == password:
                request.session['name'] = name # Обновление сессии в случае успеха
                info['name'] = name
                # переход на главную страницу зарегестрированного пользователя
                return render(request, 'home.html', context=info)
            else:
                # сообщение при неверном пароле
                info['error'] = 'Неверное имя пользователя или пароль'
        except Users.DoesNotExist: # если нет зарегестрированных пользователей
            info['error'] = 'Неверное имя пользователя или пароль'

    return render(request, 'login.html', context=info)

# функция регистрации
def register(request):
    # Берем имена пользователей
    users = Users.objects.values_list('name', flat=True)
    request.session['name'] = ' ' # обнуляем сессию
    info = {
        'error': '',
        'name': '',
    }

    if request.method == 'POST':
        # пост запрос формы регистрации
        name = request.POST.get('name')
        password = request.POST.get('password')
        r_pass = request.POST.get('r_pass')
        age = request.POST.get('age')

        # проверка заполнения всех полей
        if not name or not password or not r_pass or not age:
            info['error'] = 'Все поля обязательны для заполнения.'
            return render(request, 'register.html', context=info)

        if password != r_pass:   # проверка повторного пароля
            info['error'] = 'Пароли не совпадают' # сообщение, если они отличаются
        elif name in users: # Проверка существования пользователя
            info['error'] = 'Пользователь уже существует' # сообщение, если пользователь существует
        else:
            # Если все проверки пройдены, создаем пользователя
            user = Users(name=name, password=password, age=age)
            user.save()
            request.session['name'] = name # обновляем сессию
            info['name'] = name
            return render(request, 'home.html', context=info) # переходим на главную страницу зарегестрированного пользователя

    return render(request, 'register.html', context=info)

# функция записи на приём
def writing(request):
    doctors = Doctors.objects.all()
    writers_date = Writing.objects.values_list('date', 'time')
    name = request.session.get('name')
    info = {
        'error': '',
        'doctors': doctors,
        'name': name,
    }
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')  # Получаем id врача
        date = request.POST.get('date')
        time_1 = request.POST.get('time')
        try:
            # переделывает time из str в datetime object для дальнейшей работы
            hour, minute = map(int, time_1.split(':'))
            time_1 = time(hour, minute)
        except ValueError:
            # ошибка, если не выходит
            info['error'] = 'Неправильный формат времени.'
            return render(request, 'writing.html', context=info)

        try:
            # делаем с датой то же самое, что и со временем (из str в datetime object)
            year, month, day = map(int, date.split('-'))
            date = datetime(year, month, day)
        except ValueError:
            info['error'] = 'Неправильный формат даты.'
            return render(request, 'writing.html', context=info)

        # время работы клиники
        time_start = time(8, 0)
        time_finish = time(17, 0)

        if (datetime.date(date), time_1) in writers_date: # проверяем, свободна ли желаемая дата
            info['error'] = 'Это время уже занято'
            return render(request, 'writing.html', context=info)

        if not (time_start <= time_1 <= time_finish): # предотвращаем записи в нерабочее время
            info['error'] = 'Мы открыты с 8 до 17, попробуйте снова'
            return render(request, 'writing.html', context=info)



        # Большая проверка, не записана ли дата, которая уже прошла
        if (date.year < datetime.now().year or date.month < datetime.now().month or
                (date.month == datetime.now().month and date.day <= datetime.now().day)):
            info['error'] = 'Нельзя выбрать прошедшую дату'
            return render(request, 'writing.html', context=info)

        try:
            # Получаем объект врача по его id
            doctor = Doctors.objects.get(id=doctor_id)
            user = Users.objects.get(name=name)
            # Создаем запись
            Writing.objects.create(user=user, doctor=doctor, date=date, time=time_1)
            info['error'] = 'Вы успешно записались!'
        except Doctors.DoesNotExist:
            info['error'] = 'Врач не найден.'
        # except Exception as e:
        #     info['error'] = f'Ошибка при записи: {str(e)}'

        return render(request, 'writing.html', context=info)

    return render(request, 'writing.html', context=info)

def user_writings(request):
    # writing_of_user = Writing.objects.all()
    # name = request.session.get('name')
    # users = Users.objects.all()
    # def func(count):
    #     count += 1
    #     return count
    #
    # counter = func(0)
    # context = {
    #     'writing_of_user': writing_of_user,
    #     'name': name,
    #     'users': users,
    #     'count': func(0),
    # }
    users = Users.objects.all()  # Получение всех пользователей
    writing_of_user = Writing.objects.all()  # Получение все записи
    name = request.session.get('name') # Сессия нынешнего пользователя

    filtered_records = [] # список пользователей для их вывода в шаблоне

    # Выбираем все записи КОНКРЕТНОГО пользователя (name)
    for j in users:
        for i in writing_of_user:
            if i.user_id == j.id and j.name == name:
                filtered_records.append(i)

    context = {
        'records': filtered_records,
        'name': name,
    }

    # Отмена записи (удаление)
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        if record_id:
            record = get_object_or_404(Writing, id=record_id)
            record.delete()
        return redirect('/user/my_writings')

    return render(request, 'my_writings.html', context=context)