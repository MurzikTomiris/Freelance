from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        phone_display = self.phone if self.phone else "Нет телефона"
        return f"{self.user.username} - {phone_display}"

class Executor(UserProfile):
    # Реализуйте специфические поля/методы для Executor при необходимости
    pass

class Customer(UserProfile):
    # Реализуйте специфические поля/методы для Customer при необходимости
    pass

class Service(models.Model):
    SERVICE_CHOICES = (
        ("design", "Дизайн"),
        ("development", "Разработка"),
        ("support", "Поддержка"),
    )
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE, verbose_name="Исполнитель")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    service_type = models.CharField(max_length=11, choices=SERVICE_CHOICES, default="design", verbose_name="Тип услуги")

    def __str__(self):
        return self.name or "Неименованная услуга"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Order(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, primary_key=True, verbose_name="Услуга")
    order_type = models.CharField(max_length=11, choices=Service.SERVICE_CHOICES, default="design", verbose_name="Тип заказа")

    def __str__(self):
        return self.service.name or "Неименованный заказ"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Tag(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tags", blank=True, null=True, verbose_name="Услуга")
    # Добавьте поля, такие как имя или другие релевантные поля для модели Tag
    # Рассмотрите возможность добавления метода __str__ для значимого представления
