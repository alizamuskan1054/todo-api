from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title