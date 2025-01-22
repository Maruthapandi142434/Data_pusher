from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10)  # GET, POST, PUT
    headers = models.JSONField()

    def __str__(self):
        return f"Destination for {self.account.account_name}"
