from django.db import models


class Type(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Type'
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker'
