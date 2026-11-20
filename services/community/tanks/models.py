from django.db import models


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
    clan = models.ForeignKey(
        Clan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="players",
    )
    favorite_tank_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nickname


class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    players = models.ManyToManyField(
        Player,
        related_name="achievements",
        blank=True,
    )

    def __str__(self):
        return self.title
