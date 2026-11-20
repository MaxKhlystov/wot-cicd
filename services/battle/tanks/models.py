from django.db import models


class Battle(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("finished", "Finished"),
    ]

    map_id = models.PositiveIntegerField()
    player_ids = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    result = models.CharField(max_length=20, blank=True)
    played_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Battle {self.pk} on map {self.map_id}"
