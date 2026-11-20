from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Tank(models.Model):
    TIER_CHOICES = [(i, f"Tier {i}") for i in range(1, 11)]
    TYPE_CHOICES = [
        ("LT", "Лёгкий танк"),
        ("MT", "Средний танк"),
        ("HT", "Тяжёлый танк"),
        ("TD", "ПТ-САУ"),
        ("SPG", "САУ"),
    ]

    name = models.CharField(max_length=100, unique=True)
    nation = models.CharField(max_length=50)
    tank_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="MT",
    )
    tier = models.PositiveSmallIntegerField(
        choices=TIER_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    hp = models.PositiveIntegerField(default=1000)
    damage = models.PositiveIntegerField(default=300)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_tank_type_display()})"


class GameMap(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mode = models.CharField(max_length=50, default="Стандартный бой")
    size_km = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    max_players = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name