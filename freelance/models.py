from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        validators=[validate_slug],
    )
    phone = models.CharField(
        max_length=12, blank=True, null=True, verbose_name="Телефон"
    )

    def __str__(self):
        phone_display = self.phone if self.phone else "Нет телефона"
        return f"{self.user.username} - {phone_display}"

class Executor(UserProfile):
    # Реализуйте специфические поля/методы для Executor при необходимости
    pass

class Customer(UserProfile):
    # Пример специфического поля для Customer
    preferences = models.TextField(blank=True, verbose_name="Предпочтения")

    def __str__(self):
        return (
            super().__str__()
            + f" - Предпочтения: {self.preferences if self.preferences else 'Не указаны'}"
        )

class Service(models.Model):
    class ServicesType(models.TextChoices):
        DESIGN = "design", "Дизайн"
        DEVELOPMENT = "development", "Разработка"
        SUPPORT = "support", "Поддержка"
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE, verbose_name="Исполнитель")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    service_type = models.CharField(max_length=11, choices=ServicesType.choices, default="design", verbose_name="Тип услуги")

    def __str__(self):
        return self.name or "Неименованная услуга"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Order(models.Model):
    order_type = models.CharField(
        max_length=11,
        choices=Service.ServicesType.choices,
        default="design",
        verbose_name="Тип заказа",
    )

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создан", null=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен", null=True)
    price = models.DecimalField(
        verbose_name="Стоимость", max_digits=10, decimal_places=2, default=0
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True,
        null=True,
        verbose_name="Заказчик",
    )

    def __str__(self):
        return self.title or self.description or "Неизвестный заказ"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Tag(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tags", blank=True, null=True, verbose_name="Услуга")
    # Добавьте поля, такие как имя или другие релевантные поля для модели Tag
    # Рассмотрите возможность добавления метода __str__ для значимого представления
