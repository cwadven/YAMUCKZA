from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Foodmenu)
class Foodmenu(ImportExportModelAdmin):
    pass

@admin.register(Store)
class Store(ImportExportModelAdmin):
    pass

@admin.register(Dessertmenu)
class Dessertmenu(ImportExportModelAdmin):
    pass