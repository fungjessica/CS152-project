#import customtkinter as ctk
from utilities import clear_window
import os
import json

SAVED_RECIPES_FILE = os.path.join(os.path.dirname(__file__), "saved_recipes.json")

def load_saved_recipes():
    if os.path.exists(SAVED_RECIPES_FILE):
        try:
            with open(SAVED_RECIPES_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading saved recipes file.")
            return []
    return []

def save_recipes_to_file(recipes):
    with open(SAVED_RECIPES_FILE, "w") as file:
        json.dump(recipes, file, indent=4)

saved_recipes = load_saved_recipes()

def view_saved_recipes(root, controller):
    clear_window(root)
    saved_recipes = load_saved_recipes()

    header = ctk.CTkLabel(root, text="Saved Recipes", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    recipes_frame = ctk.CTkFrame(root)
    recipes_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def refresh_page():
        for widget in recipes_frame.winfo_children():
            widget.destroy()

        if not saved_recipes:
            empty_label = ctk.CTkLabel(recipes_frame, text="No saved recipes available.", font=("Helvetica", 16))
            empty_label.pack(pady=20, anchor="center")
        else:
            for recipe in reversed(saved_recipes):  
                recipe_frame = ctk.CTkFrame(recipes_frame, fg_color="transparent")
                recipe_frame.pack(fill="x", pady=5, padx=10)

                recipe_label = ctk.CTkLabel(recipe_frame, text=recipe, font=("Helvetica", 16))
                recipe_label.pack(side="left", fill="x", expand=True, padx=10)

                delete_button = ctk.CTkButton(
                    recipe_frame,
                    text="Delete",
                    command=lambda recipe=recipe: delete_recipe(recipe),
                    width=80,
                    height=30,
                    corner_radius=10,
                    font=("Helvetica", 12),
                    fg_color="red",
                    hover_color="darkred"
                )
                delete_button.pack(side="right", padx=10)

    refresh_page()

    input_frame = ctk.CTkFrame(root)
    input_frame.pack(pady=20)

    recipe_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter a new recipe", width=300, font=("Helvetica", 14))
    recipe_entry.pack(side="left", padx=10)

    def add_recipe():
        new_recipe = recipe_entry.get().strip()
        if new_recipe:
            saved_recipes.append(new_recipe)
            save_recipes_to_file(saved_recipes)
            recipe_entry.delete(0, "end")
            refresh_page()
        else:
            print("No recipe entered!")  

    add_button = ctk.CTkButton(
        input_frame,
        text="Add Recipe",
        command=add_recipe,
        width=100,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    add_button.pack(side="left", padx=10)

    def delete_recipe(recipe):
        if recipe in saved_recipes:
            saved_recipes.remove(recipe)
            save_recipes_to_file(saved_recipes)
        refresh_page()

    refresh_page()

    back_button = ctk.CTkButton(
        root,
        text="Back to Homepage",
        command=controller.show_homepage,
        width=150,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=20)