from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Status'
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker'
