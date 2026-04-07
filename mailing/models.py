from django.db import models


class ImportedEmail(models.Model):
    external_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=500)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Отправленное письмо'
        verbose_name_plural = 'Отправленные письма'

    def __str__(self):
        return f"{self.email} - {self.subject[:50]}"


class ImportError(models.Model):
    row_number = models.IntegerField()
    external_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField()
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ошибка импорта'
        verbose_name_plural = 'Ошибки импорта'

    def __str__(self):
        return f"Строка {self.row_number}: {self.error_message[:100]}"