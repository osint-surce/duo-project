from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    artist = models.CharField(max_length=150, verbose_name="Артист")
    date = models.DateTimeField(verbose_name="Дата и время")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена от")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    image = models.ImageField(
        upload_to='events/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-date']          # Новые сверху
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.artist} — {self.title}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None
