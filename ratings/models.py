from django.db import models

from freelance.models import Order, UserProfile


class RatingOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    testimonial = models.TextField(verbose_name = "Отзыв", blank=True, null=True)
    order_rating = models.FloatField(verbose_name = "Ретинг", blank=True, null=True)

    class Meta:
        unique_together = ("order", "user")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"



