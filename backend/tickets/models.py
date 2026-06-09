from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Город')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name='Категория')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name='Город')
    venue = models.CharField(max_length=200, verbose_name='Место проведения')
    date = models.DateTimeField(verbose_name='Дата и время')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена билета')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Изображение')
    total_tickets = models.PositiveIntegerField(default=100, verbose_name='Всего билетов')
    tickets_sold = models.PositiveIntegerField(default=0, verbose_name='Продано билетов')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['date']

    def __str__(self):
        return self.title

    @property
    def tickets_left(self):
        return self.total_tickets - self.tickets_sold

    @property
    def is_available(self):
        return self.tickets_left > 0


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'.strip() or self.user.username

    @property
    def tickets_bought(self):
        return self.user.orders.filter(status='paid').count()

    @property
    def upcoming_events(self):
        from django.utils import timezone
        return self.user.orders.filter(status='paid', event__date__gte=timezone.now()).count()

    @property
    def favorite_count(self):
        return self.user.favorites.count()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Корзина'

    @property
    def total_price(self):
        return self.event.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.event.title}'

