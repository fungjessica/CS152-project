import json
import os
import customtkinter as ctk
from utilities import clear_window

selected_recipe = None

def load_recipes():
    """Load recipe categories from the static `recipes.json` file."""
    file_path = os.path.join(os.path.dirname(__file__), 'recipes.json')
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return {}
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return {}

def browse_recipes(root, controller):
    """Allows users to browse available recipes."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Browse Recipes", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    # Main container frame for the layout
    main_container = ctk.CTkFrame(root)
    main_container.pack(pady=10, padx=10, fill="both", expand=True)

    # Adjust the grid weights to control how much space each frame takes
    main_container.grid_columnconfigure(0, weight=1)  # Sidebar
    main_container.grid_columnconfigure(1, weight=3)  # Main content frame (higher weight = takes more space)
    main_container.grid_rowconfigure(0, weight=1)     # Makes both frames expand vertically

    # Sidebar frame on the left for navigation buttons
    sidebar_frame = ctk.CTkFrame(main_container, width=200, height=600, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    # Load recipe categories from the JSON file
    recipe_data = load_recipes()

    # Frame for displaying recipes in the main area
    recipes_frame = ctk.CTkFrame(main_container)
    recipes_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def show_recipes(category):
        """Display recipes for the selected category."""
        global selected_recipe
        for widget in recipes_frame.winfo_children():
            widget.destroy()

        header.configure(text=f"{category} Recipes")

        if category in recipe_data:
            recipes = recipe_data[category]
            for idx, item in enumerate(recipes):
                row = idx // 3  # Calculate the current row
                column = idx % 3  # Calculate the current column (0, 1, 2 for each row)
                item_button = ctk.CTkButton(
                    recipes_frame,
                    text=item,
                    font=("Helvetica", 14),
                    command=lambda recipe=item: set_selected_recipe(recipe),
                    fg_color="transparent",
                    border_width=0
                )
                item_button.grid(row=row, column=column, padx=40, pady=20)

    # Add category buttons to the sidebar
    for category in recipe_data.keys():
        ctk.CTkButton(
            sidebar_frame,
            text=category,
            command=lambda cat=category: show_recipes(cat),
            width=120,
            height=40,
            corner_radius=10
        ).pack(pady=10, padx=10, anchor="w")

    # Save recipe button
    save_button = ctk.CTkButton(
        sidebar_frame,
        text="Save Recipe",
        command=lambda: save_recipe(controller),
        width=120,
        height=40,
        corner_radius=10
    )
    save_button.pack(pady=20, padx=10, anchor="w")

    # Back to homepage button
    back_button = ctk.CTkButton(
        sidebar_frame,
        text="Back to Homepage",
        command=controller.show_homepage,
        width=120,
        height=40,
        corner_radius=10
    )
    back_button.pack(pady=40, padx=10, anchor="w")

# Function to select a recipe
def set_selected_recipe(recipe):
    global selected_recipe
    selected_recipe = recipe
    print(f"Selected recipe: {selected_recipe}")

# Function to save the selected recipe
def save_recipe(controller):
    global selected_recipe
    if selected_recipe:
        if selected_recipe not in controller.saved_recipes:
            controller.saved_recipes.append(selected_recipe)
            controller.save_data(controller.saved_recipes, "saved_recipes.json")
            print(f"Saved recipe: {selected_recipe}")
        else:
            print("Recipe is already saved.")
    else:
        print("No recipe selected.")
