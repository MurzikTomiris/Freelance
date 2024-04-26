
# validators.py
from django.core.exceptions import ValidationError

def validate_username(value):
    # Ваш код валидации имени пользователя
    if not value.isalnum():
        raise ValidationError("Имя пользователя должно состоять только из букв и цифр.")
    if len(value) < 8 or len(value) > 20:
        raise ValidationError("Имя пользователя должно содержать от 8 до 20 символов.")
    # Дополнительные проверки, если необходимо
    