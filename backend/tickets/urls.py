from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.index, name='index'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:event_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('favorite/<int:event_id>/', views.toggle_favorite, name='toggle_favorite'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
