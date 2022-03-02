from django.core.mail import send_mail
from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
# from .tasks import order_created


def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер. {order_id}'
    message = f'Дорогой. {order.first_name},\n\nВы успешно разместили заказ.\
                Номер вашего заказа {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'dostavimvdom2@gmail.com',
                          [order.email])
    return mail_sent


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         comic=item['comic'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            # запуск асинхронной задачи
            order_created(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
