from threading import Thread
import requests


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
    x = requests.post(url='https://papayes.cf/user/register/', data=post_data)
    return x.status_code



@threaded
def save_korzina(message, product, price, count):
    post_data = {
        'user_id': message.from_user.id,
        'product': product,
        'price': price,
        'count': count,
    }
    requests.post(url='https://papayes.cf/korzina/create/', data=post_data)


@threaded
def del_korzina(pk):
    requests.delete(url=f'https://papayes.cf/korzina/delete/{pk}')


def Create_order(product, price, address, number, user) -> int():
    data = {
        "product": f"{product}",
        "price": f"{price}",
        "address": f"{address}",
        "number": f"{number}",
        "order": 'Kutilmoqda',
        "user": user
    }
    x = requests.post(url='https://papayes.cf/order/', data=data)
    return x.status_code
