from django.shortcuts import render, redirect
import json, random, openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def landing(request):
    if str(request.user) == "AnonymousUser":
        return render(request, "welcomepage.html")
    else:
        return render(request, "foodie_app/home.html")


def signup(request):

    if request.method == "POST":
        form = ProfileCreationForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.error_messages)
         
    else:
        form = ProfileCreationForm()
        return render(request, "account/signup.html", {"form": form})

    return render(request, "account/signup.html", {"form" : form})

def user_login(request):
    if request.method == "POST":
        form = ProfileAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if(user is not None):
                login(request, user)
                return redirect('home')
            
            else:
                form.add_error(None, "Invalid Login Credentials")

    else:
        form = ProfileAuthenticationForm()

    context = {
        "form" : form
    }

    return render(request, "account/login.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def results(request):

    ings = request.POST.get('ings', '')

    ingredients = ings.replace("_", ",")

    data = api(ingr=ingredients)

    #Convert to String and split
    ingredient = str(data).split("~")[0].split("-")[1:]

    instructions = str(data).split("~")[1:]

    context = {
        "ingredients" : ingredient,
        "instructions" : instructions
    }

    return render(request, "foodie_app/results.html", context)



@login_required
def profile(request):

    user = request.user

    if request.method == "POST":
        form = UpdateProfile(data=request.POST, instance=user)
        password = request.POST.get('password')
        #print(f"form submitted {password}")

        if(user.check_password(password)):
            
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile is updated successfully")

            else:
                messages.error(request, "something went wrong")
            return redirect("profile")    
            
        else:
            return render(request, "account/profile.html", {"form" : form, "user" : user})
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = UpdateProfile(initial=initial_data)
        
    context = {
        "form" : form,
        "user" : user
    }

    return render(request, "account/profile.html", context)



@login_required
def saverecipe(request):
    ingredients = request.POST.getlist('ingredients')
    instructions = request.POST.getlist('instructions')
    
    for i in ingredients:
        print(f" ingredients {i}")

    title = request.POST.get("title")

    recipe = Recipe(recipe_name = title)
    recipe.set_ingredients(ingredients)
    recipe.set_instructions(instructions)
    recipe.save()


    save_ingredients(recipe.get_ingredients())
    
    fav = Favourite_Recipe(recipe_id = recipe, user_id = request.user)
    fav.save()

    messages.success(request,"Successfully saved recipe")
    return redirect("home")


@login_required
def savedrecipe(request):

    fav_recipes = Favourite_Recipe.objects.filter(user_id = request.user)

    context = {
        "favs" : fav_recipes,
        "size" : len(fav_recipes)
    }

    return render(request, "foodie_app/saved_recipe.html", context)

def savedRecipeDetails(request, recipe_id):
    
    favs = Favourite_Recipe.objects.get(pk=recipe_id)
    user = request.user
    context = {
        "fav" : favs,
        "user" : user
    }

    return render(request, "foodie_app/recipe_details.html", context)

def deleteSavedRecipe(request, recipe_id):
    if request.method == "POST":
        recipe = Favourite_Recipe.objects.get(pk=recipe_id)
        delete_user_ingredients(recipe.recipe_id.get_ingredients(), request.user)
        recipe.delete()
        messages.success(request, "Successfully deleted recipe from favourite recipes")
        return redirect('saved_recipe')


def editSavedRecipe(request, recipe_id):
    recipe = Favourite_Recipe.objects.get(pk=recipe_id)
    context = {

    }

    if request.method == "POST":
        notes = request.POST.get("notes")
        recipe.notes = notes
        recipe.save()
        messages.success(request, "Successfully Edited Recipe")
        return redirect("saved_recipe")

    context = {
        "recipe" : recipe,
        "recipe_id" : recipe_id
    }
    
    return render(request, "foodie_app/edit_recipe_details.html", context)

def suggestedRecipes(request):
    recipes = Recipe.objects.all()

    #shuffle and get 5 only
    random_recipes = random.sample(list(recipes), min(len(recipes), 5))

    context = {
        "recipes" : random_recipes,
        "size" : len(recipes)
    }
    
    return render(request, "foodie_app/suggested_recipes.html", context)


def randomRecipeDetails(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    user = request.user

    user_recipes = Favourite_Recipe.objects.filter(user_id = user)
    found = False

    for rec in user_recipes:
        if recipe_id == rec.recipe_id.recipe_id:
            found = True

    
    context = {
        "recipe" : recipe,
        "user" : user,
        "found" : found
    }

    return render(request, "foodie_app/random_recipe_details.html", context)



#Additional
def AddToFav(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    user = request.user

    favs = Favourite_Recipe(recipe_id=recipe, user_id = user)
    favs.save()

    save_ingredients(recipe.get_ingredients(), recipe, user)
    return redirect("saved_recipe")


def api(ingr):
    openai.api_key = "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"
    prompt = "Generate a step by step recipe that strictly contains the following ingredients(use the metric system for the measurements but do not include measurements under ingredients but include them under instructions)(another key to note, for each step of the recipe, put a '~' before numbering each step of the recipe)(put the heading instructions after naming all ingredients):"
    #user_input = input("Enter the ingredidience here: ")
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role" : "user", "content" : prompt + " " + ingr}]
    )

    data = json.loads(str(completion))
    return data['choices'][0]['message']['content']
    



def save_ingredients(ingredients, rec, user):
    for ings in ingredients:
        ing = Ingredient.objects.get_or_create(ingredient_name = ings)
        save_user_ingredients(ing, user)
        save_recipe_ingredients(ing, rec)

    pass

def save_user_ingredients(ingredients, user):
    user_ings = User_Ingredient(ingredient_id = ingredients, user_id = user)
    user_ings.save()



def save_recipe_ingredients(ingredients, recipe):
    rec = Recipe_Ingredients(ingredient_id = ingredients, recipe_id = recipe)
    rec.save()


def delete_user_ingredients(ingredients, user):
    for ings in ingredients:
        try:
            ing = User_Ingredient.objects.get(ingredient_id = ings, user_id = user)
            ing.delete()
        except Exception as e:
            pass
