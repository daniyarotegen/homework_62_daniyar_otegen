from django.db import models
from django.utils import timezone


class Issue(models.Model):
    summary = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Summary'
    )
    description = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
        verbose_name='Description'
    )
    project = models.ForeignKey(
        to='tracker.Project',
        related_name='issues',
        null=False,
        blank=False,
        on_delete=models.RESTRICT
    )
    status = models.ForeignKey(
        to='tracker.Status',
        related_name='issues',
        null=False,
        blank=False,
        on_delete=models.RESTRICT
    )
    type = models.ManyToManyField(
        to='tracker.Type',
        related_name='issues',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Time created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Time updated'
    )
    is_deleted = models.BooleanField(
        verbose_name='Deleted',
        null=False,
        default=False
    )
    deleted_at = models.DateTimeField(
        verbose_name='Deletion time',
        null=True,
        default=None
    )

    def __str__(self):
        return self.summary

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        app_label = 'tracker'
