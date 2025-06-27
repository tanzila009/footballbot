from django.db import models

class Player(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    is_registered_for_game = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.full_name} ({self.phone})"

class GameRegistration(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает чек"),
        ("verified", "Подтверждено"),
        ("expired", "Просрочено"),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    receipt_file_id = models.CharField(max_length=255, blank=True, null=True)
