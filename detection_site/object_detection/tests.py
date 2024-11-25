from datetime import datetime, time
from tkinter.font import names

from django.test import TestCase, Client
from django.urls import reverse
from .models import *
# Create your tests here.

class ViewsTextCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = Users.objects.create(name='testuser', password='password123')


    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('doctors', response.context)
        self.assertIn('name', response.context)


    def test_home_log_view(self):
        response = self.client.get(reverse('users'))  # Замените 'home_log' на имя вашего URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('doctors', response.context)
        self.assertIn('name', response.context)


    def test_login_view_success(self):
        response = self.client.post(reverse('login'), {
            'name': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('name', response.context)
        self.assertEqual(response.context['name'], 'testuser')


    def test_login_view_failure(self):
        response = self.client.post(reverse('login'), {
            'name': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Неверное имя пользователя или пароль')


    def test_login_view_user_not_found(self):
        response = self.client.post(reverse('login'), {
            'name': 'nonexistentuser',
            'password': 'somepassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Неверное имя пользователя или пароль')


    def test_register_view_create_user(self):
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('name', response.context)
        self.assertEqual(response.context['name'], 'newtestuser')

    def test_register_view_not_all_fields(self):
        # тест при не вводе возраста
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Все поля обязательны для заполнения.')

        # тест при не вводе пароля
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': '',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Все поля обязательны для заполнения.')

        # тест при не вводе имени
        response = self.client.post(reverse('register'), {
            'name': '',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Все поля обязательны для заполнения.')

        # тест при не вводе повторения пароля
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': '',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Все поля обязательны для заполнения.')

    def test_register_view_check_r_pass(self):
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword2222',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Пароли не совпадают')

    def test_register_view_check_user_in_users(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword222',
            'r_pass': 'newtestuserpassword222',
            'age': 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Пользователь уже существует')

    def test_writing_view_create(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Doctors.objects.all()
        Doctors.objects.create(name='testDoc', description= 'BEST TEST', age='45', price=2500)
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30',
            'time': '08:30',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Вы успешно записались!')

    def test_writing_view_check_time(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Doctors.objects.all()
        Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30',
            'time': '8:30:00', # Проверка формата времени
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Неправильный формат времени.')

    def test_writing_view_check_date(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Doctors.objects.all()
        Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30 00:00:00', # Проверка формата Даты
            'time': '08:30',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Неправильный формат даты.')

    def test_writing_view_check_work_time(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Doctors.objects.all()
        Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30',
            'time': '19:15', # Берем запись вне рабочего времени
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Мы открыты с 8 до 17, попробуйте снова')

    def test_writing_view_check_not_free_time(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Users.objects.all()
        user = Users.objects.create(name='newtestuser2', password='newtestuserpassword2', age=25)
        Doctors.objects.all()
        doctor = Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        Writing.objects.create(user=user, doctor=doctor, date='2024-11-30', time='16:15')
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30',
            'time': '16:15', # Берём то же время, что уже есть
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Это время уже занято')


    def test_writing_view_check_past_date(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Doctors.objects.all()
        doctor = Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-20', # берём прошедшую дату
            'time': '16:15',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Нельзя выбрать прошедшую дату')

    def test_writing_view_check_delete(self):
        response_1 = self.client.post(reverse('register'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword',
            'r_pass': 'newtestuserpassword',
            'age': 20,
        })
        response_2 = self.client.post(reverse('login'), {
            'name': 'newtestuser',
            'password': 'newtestuserpassword'
        })
        Users.objects.all()
        user = Users.objects.create(name='newtestuser2', password='newtestuserpassword2', age=25)
        Doctors.objects.all()
        doctor = Doctors.objects.create(name='testDoc', description='BEST TEST', age='45', price=2500)
        Writing.objects.create(user=user, doctor=doctor, date='2024-11-30', time='16:15')
        response = self.client.post(reverse('writing'), {
            'doctor_id': '1',
            'date': '2024-11-30',
            'time': '16:30', # Берём то же время, что уже есть
        })
        a = len(Writing.objects.all()) # Количество записей на приём для пользователя
        self.assertEqual(a, 2)
        response_delete = self.client.post(reverse('user_writings'), {
            'record_id': 1,
        }) # удаляем первую запись
        a = len(Writing.objects.all()) # Обновляем значение
        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(a, 1)
