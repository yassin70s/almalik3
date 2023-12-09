from collections.abc import MutableMapping
from typing import Any
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

class MainMixin(models.Model):
    is_setting = False
    is_report = False
    is_view = False
    is_api = True
    is_admin = True
    
    class Meta:
        abstract = True
    name = None
    
class GroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    def dd(self):
        return self


class GroupMixin(MainMixin):
    objects = GroupManager()
    is_group = True
    codename_group_permissions = []
    class Meta:
        abstract = True
    def group(self):
        return auth_models.Group.objects.get(name = self.group_model_name())
    def group_model_name(self):
        return f"{self._meta.app_label}_{self._meta.model_name}"
    def create_group_model(self):
        group = auth_models.Group.objects.update_or_create(name = self.group_model_name())[0].permissions.set(
            auth_models.Permission.objects.filter(codename__in = self.codename_group_permissions)
        )
    



class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    def create(self, **kwargs):
        print(44556677)
        return super().create(**kwargs)
    
    
    
    
class UserMixin(GroupMixin):
    username = None
    password = None
    first_name = None
    last_name = None
    is_active = True,
    is_staff = True,
    name = None

    objects = UserManager()
    def model_username(self):
        return f"{self._meta.app_label[:1].capitalize()}{self._meta.model_name[:1].capitalize()}{self.pk}"
    def model_first_name(self):
        if not self.name:
            return f"{self._meta.verbose_name} | {self.model_username()}"
        else:
            return self.name
    def model_password(self):
        return "123456789"
    def user(self):
        return auth_models.User.objects.get(username = self.model_username())
    def create_user(self,):
        user = auth_models.User.objects.filter(username = self.model_username())
        print(user,6777)
        if not user.exists():
            auth_models.User.objects.create_user(
                username = self.username or self.model_username(),
                password =self.password or  self.model_password(),
                first_name= self.first_name or self.model_first_name(),
                last_name = self.last_name,
                is_active = self.is_active,
                is_staff = self.is_staff,
                
            ).groups.add(
                self.group(),
            )
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.create_user()
        


    

    class Meta:
        abstract = True


class User(UserMixin):
    pass
    
    

class Setting(MainMixin):
    is_view = True
    class Meta:
        verbose_name = ("Setting")
        verbose_name_plural = ("Settings")

class Report(MainMixin):
    is_view = True
    class Meta:
        verbose_name = ("report")
        verbose_name_plural = ("reports")

