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
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")

    def __str__(self):
        phone_display = self.phone if self.phone else "Нет телефона"
        return f"{self.user.username} - {phone_display}"


class Executor(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name="Профиль",
    )
    skills = models.TextField(blank=True, verbose_name="Навыки")
    avatar = models.ImageField(
        upload_to="user_avatars", null=True, blank=True, verbose_name="Аватар"
    )

    def __str__(self):
        return (
            super().__str__()
            + f" - Навыки: {self.skills if self.skills else 'Не указаны'}"
        )

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


class Customer(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name="Профиль",
    )
    preferences = models.TextField(blank=True, verbose_name="Предпочтения")

    def __str__(self):
        return f"{self.profile.user.username} - email: {self.profile.user.email if self.profile.user.email else 'Не указаны'}"

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Service(models.Model):
    class ServicesType(models.TextChoices):
        DESIGN = "design", "Дизайн"
        DEVELOPMENT = "development", "Разработка"
        SUPPORT = "support", "Поддержка"

    executor = models.ForeignKey(
        Executor, on_delete=models.CASCADE, verbose_name="Исполнитель"
    )
    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Название"
    )
    description = models.TextField(verbose_name="Описание")
    service_type = models.CharField(
        max_length=11,
        choices=ServicesType.choices,
        default="design",
        verbose_name="Тип услуги",
    )
    price = models.DecimalField(
        verbose_name="Стоимость", max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return self.name or "Неименованная услуга"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Order(models.Model):
    # service = models.OneToOneField(
    #     Service, on_delete=models.CASCADE, primary_key=True, verbose_name="Услуга"
    # )
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
        related_name="customers",
        blank=True,
        null=True,
        verbose_name="Заказчик",
    )

    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="executors",
        blank=True,
        null=True,
        verbose_name="Исполнитель",
    )

    def __str__(self):
        return self.title or self.description or "Неизвестный заказ"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderRequest(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="requests", verbose_name="Заказ"
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="order_requests",
        verbose_name="Исполнитель",
        default=None,
        null=True,
    )
    about_executor = models.TextField(
        verbose_name="Об исполнителе", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "В ожидании"),
            ("accepted", "Принято"),
            ("rejected", "Отклонено"),
        ],
        default="pending",
        verbose_name="Статус",
    )

    class Meta:
        unique_together = ("order", "executor")
        verbose_name = "Заявка на заказ"
        verbose_name_plural = "Заявки на заказы"

    def __str__(self):
        return f"{self.order.title} - {self.executor.profile.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя тега")
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="tags",
        blank=True,
        null=True,
        verbose_name="Услуга",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
