from import_export import resources
from .models import Person
from import_export import resources

class FoodmenuResource(resources.ModelResource):
    class Meta:
        model = Foodmenu