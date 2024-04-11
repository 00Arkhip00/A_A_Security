from django.db import models


class Users(models.Model):
    login = models.TextField()
    password = models.IntegerField()


class Message(models.Model):
    name = models.TextField()
    sms = models.JSONField()