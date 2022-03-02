from decimal import Decimal
from django.conf import settings

from comics_site.models import Comic


class Cart(object):
    def __init__(self, request):
        """
        Инициализируем "Корзину" - Избранное
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, comics, quantity=1, update_quantity=False):
        """
            Добавить комикс в избранное или обновить его количество.
        """
        comics_id = str(comics.id)
        if comics_id not in self.cart:
            self.cart[comics_id] = {'quantity': 0,
                                    'price': str(comics.price)}
        if update_quantity:
            self.cart[comics_id]['quantity'] = quantity
        else:
            self.cart[comics_id]['quantity'] += quantity
        self.save()

    def __iter__(self):
        """
        Перебор комиксов в избранном и получение комиксов из базы данных.
        """
        comics_ids = self.cart.keys()
        # получение объектов comic и добавление их в корзину
        comics = Comic.objects.filter(id__in=comics_ids)
        for comic in comics:
            self.cart[str(comic.id)]['comic'] = comic

        for item in self.cart.values():
            item['price'] = Decimal(item['comic'].price)
            item['total_price'] = item['comic'].price * item['quantity']
            yield item

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, comics):
        """
        Удаление из избраного
        """
        comics_id = str(comics.id)
        if comics_id in self.cart:
            del self.cart[comics_id]
            self.save()

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление избранного из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
