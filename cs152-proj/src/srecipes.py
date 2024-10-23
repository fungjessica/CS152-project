import customtkinter as ctk
from utilities import clear_window
from recipe_data import saved_recipes

def view_saved_recipes(root, controller):
    """Displays the saved recipes."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Saved Recipes", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    if not saved_recipes:
        empty_label = ctk.CTkLabel(root, text="No saved recipes available.", font=("Helvetica", 16))
        empty_label.pack(pady=20)
    else:
        for recipe in saved_recipes:
            recipe_label = ctk.CTkLabel(root, text=recipe, font=("Helvetica", 16))
            recipe_label.pack(pady=10)

    # Back to homepage button
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
