from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Name'
    )
    description = models.TextField(
        max_length=3000,
        blank=True,
        verbose_name='Description'
    )
    start_date = models.DateField(
        verbose_name='Start date'
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='End date'
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tracker'
