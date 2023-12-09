from main.api import *
from . import admin


class EntryApi(ModelApi,admin.EntryAdmin):
    pass