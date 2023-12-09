from django.db import models
from main.models import MainMixin




class My(MainMixin,models.Model):
    view = True
    admin = True
    report = True
    group = True
