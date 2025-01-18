from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)  # Поле для отслеживания состояния комнаты

    def close(self):
        self.is_open = False
        self.save()

    def delete(self, *args, **kwargs):
        # Здесь можно добавить другую логику перед удалением, если это необходимо
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name