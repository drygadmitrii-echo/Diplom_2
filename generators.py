from faker import Faker
import random
import string

fake = Faker('ru_RU')

def generate_username():
    return fake.user_name()

def generate_secure_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for i in range(length))

def generate_email():
    domains = ['mail.ru', 'yandex.ru', 'gmail.com', 'hotmail.com']
    return fake.user_name() + '@' + random.choice(domains)

def generate_comment():
    return fake.text(max_nb_chars=20)