from django.db import models
from django.contrib.auth.models import AbstractUser
import json
from django.contrib.auth import get_user_model




# Create your models here.
class Profile(AbstractUser):
    class Meta:
        app_label = "foodie_app"

    def __str__(self):
        return self.username
    

class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=70)

    def __str__(self):
        return self.ingredient_name
    

class User_Ingredient(models.Model):
    user_ingredient_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_ingredient_id}"



class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_name = models.CharField(max_length=70)
    instruction_details = models.TextField(blank =True)
    ingredient_details = models.TextField(blank =True)

    def __str__(self):
        return self.recipe_name


    def set_ingredients(self, ingredients_list):
        self.ingredient_details = json.dumps(ingredients_list)
    
    def set_instructions(self, instructions_list):
        self.instruction_details = json.dumps(instructions_list)


    def get_instructions(self):
        return json.loads(self.instruction_details)
    
    def get_ingredients(self):
        return json.loads(self.ingredient_details)

    def __str__(self):
        return self.recipe_name

class Recipe_Ingredients(models.Model):
    recipe_ingredient_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe_ingredient_id}"

    
class Favourite_Recipe(models.Model):
    favourite_recipe_id = models.AutoField(primary_key=True)
    date_added = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    recipe_id = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'recipe_id')

    def __str__(self):
        return f"{self.user_id.username} {self.recipe_id.recipe_name}"