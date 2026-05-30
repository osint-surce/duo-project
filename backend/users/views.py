from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Пользователь уже существует"},
            status=400
        )

    User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message": "Успешная регистрация"
    })
