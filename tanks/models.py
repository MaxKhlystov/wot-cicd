from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    tank_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="MT")
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(10)])
    hp = models.PositiveIntegerField(default=1000)
    damage = models.PositiveIntegerField(default=300)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_tank_type_display()})"


class Clan(models.Model):
    tag = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tag}] {self.name}"


class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    level = models.PositiveIntegerField(default=1)
    experience = models.BigIntegerField(default=0)
    credits = models.BigIntegerField(default=0)
    clan = models.ForeignKey(Clan, null=True, blank=True, on_delete=models.SET_NULL, related_name="players")
    favorite_tank = models.ForeignKey(Tank, null=True, blank=True, on_delete=models.SET_NULL, related_name="fans")

    def __str__(self):
        return self.nickname


class GameMap(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mode = models.CharField(max_length=50, default="Стандартный бой")
    size_km = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    max_players = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class Battle(models.Model):
    STATUS_CHOICES = [("planned", "Запланирован"), ("ongoing", "Идёт"), ("finished", "Завершён")]

    map = models.ForeignKey(GameMap, on_delete=models.CASCADE, related_name="battles")
    players = models.ManyToManyField(Player, related_name="battles")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    result = models.CharField(max_length=20, blank=True)  # "victory", "defeat", "draw"
    played_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Бой на {self.map.name} ({self.get_status_display()})"


class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    players = models.ManyToManyField(Player, related_name="achievements", blank=True)

    def __str__(self):
        return self.title
