from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Event, Category, City, CartItem, Order, Favorite, UserProfile



def index(request):
    category_slug = request.GET.get('category')
    city_id = request.GET.get('city')

    events = Event.objects.select_related('category', 'city').all()

    if category_slug:
        events = events.filter(category__slug=category_slug)
    if city_id:
        events = events.filter(city_id=city_id)

    categories = Category.objects.all()
    cities = City.objects.all()
    active_category = category_slug or 'all'

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = request.user.cart_items.count()

    return render(request, 'tickets/index.html', {
        'events': events,
        'categories': categories,
        'cities': cities,
        'active_category': active_category,
        'cart_count': cart_count,
    })



@login_required
def cart(request):
    cart_items = request.user.cart_items.select_related('event').all()
    total = sum(item.total_price for item in cart_items)
    return render(request, 'tickets/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
@require_POST
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    item, created = CartItem.objects.get_or_create(user=request.user, event=event)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'Билет на «{event.title}» добавлен в корзину')
    return redirect('tickets:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('tickets:cart')


@login_required
@require_POST
def checkout(request):
    cart_items = request.user.cart_items.select_related('event').all()
    if not cart_items:
        messages.error(request, 'Корзина пуста')
        return redirect('tickets:cart')

    for item in cart_items:
        if not item.event.is_available:
            messages.error(request, f'Билеты на «{item.event.title}» закончились')
            return redirect('tickets:cart')
        Order.objects.create(
            user=request.user,
            event=item.event,
            quantity=item.quantity,
            total_price=item.total_price,
            status='paid',
        )
        item.event.tickets_sold += item.quantity
        item.event.save()

    cart_items.delete()
    messages.success(request, 'Оплата прошла успешно! Билеты в вашем профиле.')
    return redirect('tickets:profile')



@login_required
def profile(request):
    from django.utils import timezone

    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    orders = request.user.orders.select_related('event').filter(status='paid')
    now = timezone.now()

    upcoming_orders = orders.filter(event__date__gte=now)
    past_orders = orders.filter(event__date__lt=now)
    favorites = request.user.favorites.select_related('event').all()

    return render(request, 'tickets/profile.html', {
        'profile': profile_obj,
        'upcoming_orders': upcoming_orders,
        'past_orders': past_orders,
        'favorites': favorites,
    })


@login_required
@require_POST
def edit_profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    user = request.user

    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    user.email = request.POST.get('email', '')
    user.save()

    profile_obj.phone = request.POST.get('phone', '')
    city_id = request.POST.get('city')
    if city_id:
        profile_obj.city_id = city_id
    profile_obj.save()

    messages.success(request, 'Профиль обновлён')
    return redirect('tickets:profile')


@login_required
@require_POST
def toggle_favorite(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, event=event)
    if not created:
        fav.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tickets:index')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('tickets:index')
        else:
            messages.error(request, 'Неверный email или пароль')

    return render(request, 'tickets/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('tickets:index')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        city_id = request.POST.get('city')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
        else:
            username = email.split('@')[0]
            base = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{counter}'
                counter += 1

            user = User.objects.create_user(username=username, email=email, password=password)
            profile_obj = UserProfile.objects.create(user=user)
            if city_id:
                profile_obj.city_id = city_id
                profile_obj.save()

            login(request, user)
            messages.success(request, 'Аккаунт создан!')
            return redirect('tickets:index')

    cities = City.objects.all()
    return render(request, 'tickets/register.html', {'cities': cities})


def logout_view(request):
    logout(request)
    return redirect('tickets:index')

