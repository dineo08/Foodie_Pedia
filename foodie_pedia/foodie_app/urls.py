from django.urls import path
from .views import *


urlpatterns = [
    
    #Authentication
    path('signup', signup, name='sign_up'),
    path('login', user_login, name="login"),

    #Navbar
    path('', landing, name='home'),
    path('suggested_recipes', suggestedRecipes, name='suggested_recipes'),
    path('saved_recipe', savedrecipe, name='saved_recipe'),
    path('profile', profile, name='profile'),
    path('logout', logout_user, name='logout'),


    #Functions
    path('saverecipe', saverecipe, name='saverecipe'),
    path('results', results, name='results'),
    

    #Fav recipes
    path('saved_recipe_details/<int:recipe_id>', savedRecipeDetails, name="saved_recipe_details"),
    path('random_recipe_details/<int:recipe_id>', randomRecipeDetails, name="random_recipe_details"),
    path('edit_saved_recipe/<int:recipe_id>', editSavedRecipe, name="edit_saved_recipe"),
    path('delete_saved_recipe/<int:recipe_id>', deleteSavedRecipe, name="delete_saved_recipe"),
    


    #Additional 
    path('add_to_fav/<int:recipe_id>', AddToFav, name="add_to_fav")
]
