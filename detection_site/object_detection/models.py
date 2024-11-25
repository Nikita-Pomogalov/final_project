from django.db import models

# Модель доктора с его именем, описанием, ценой за приём и фото
class Doctors(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    age = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images', default='images/anonim.png')

    def __str__(self):
        return self.name

# По этой модели проходитрегистрация
class Users(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    age = models.IntegerField(max_length=3, default=21)

    def __str__(self):
        return self.name

# Модель для входа в систему
class UsersLogin(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=200)

# Модель записи на приём
class Writing(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'Запись {self.user} к {self.doctor} на {self.date} в {self.time}'
