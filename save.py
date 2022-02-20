from threading import Thread
from loader import dp
import requests

from utils import on_startup_notify


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def save_user(message, number=None, address=None) -> int():
    post_data = {
        'tg_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'number': number,
        'address': address,
    }
    x = requests.post(url='http://127.0.0.1:8000/user/register/', data=post_data)
    return x.status_code


@threaded
def save_order(order):
    requests.post(url='http://127.0.0.1:8000//order/', data=order)


@threaded
def comment_post(order):
    requests.post(url='http://127.0.0.1:8000//order/', data=order)


@threaded
def save_korzina(message, product, price, count):
    post_data = {
        'user_id': message.from_user.id,
        'product': product,
        'price': price,
        'count': count,
    }
    requests.post(url='http://127.0.0.1:8000/korzina/create/', data=post_data)


@threaded
def del_korzina(pk):
    requests.delete(url=f'http://127.0.0.1:8000/korzina/delete/{pk}')
