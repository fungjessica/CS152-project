import json
import os
import customtkinter as ctk
from utilities import clear_window
<<<<<<< HEAD

selected_recipe = None

=======
from recipe_data import saved_recipes
from PIL import Image

>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88
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
    clear_window(root)

    header = ctk.CTkLabel(root, text="Browse Recipes", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    main_container = ctk.CTkFrame(root)
    main_container.pack(pady=10, padx=10, fill="both", expand=True)

    sidebar_frame = ctk.CTkFrame(main_container, width=125, height=600, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    sidebar_frame.grid_propagate(False)
    sidebar_frame.pack_propagate(False)

    main_container.grid_columnconfigure(0, weight=0, minsize=100) 
    main_container.grid_columnconfigure(1, weight=1)  
    main_container.grid_rowconfigure(0, weight=1)  

    recipe_data = load_recipes()

<<<<<<< HEAD
    # Frame for displaying recipes in the main area
    recipes_frame = ctk.CTkFrame(main_container)
    recipes_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
=======
    def show_recipes(category=None, search_query=""):
        global selected_recipe
>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88

    def show_recipes(category):
        """Display recipes for the selected category."""
        global selected_recipe
        for widget in recipes_frame.winfo_children():
            widget.destroy()

        header.configure(text="Recipes")

<<<<<<< HEAD
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
=======
        if category:
            recipes_to_display = recipe_data.get(category, [])
        else:
            recipes_to_display = []
            for category, recipes in recipe_data.items():
                for recipe in recipes:
                    if search_query.lower() in recipe.lower():
                        recipes_to_display.append(recipe)

        for idx, item in enumerate(recipes_to_display):
            row = idx // 4
            column = idx % 4

            image_path = os.path.join(os.path.dirname(__file__), "images", item["image"])
            item_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))  
            
            item_button = ctk.CTkButton(
                recipes_frame, 
                image=item_image,
                compound="top",
                text=item["name"], 
                font=("Helvetica", 14),
                command=lambda item=item: set_selected_recipe(item),  
                fg_color="transparent",
                border_width=0
            )
            item_button.grid(row=row, column=column, padx=60, pady=60)

    button1 = ctk.CTkButton(
        sidebar_frame, 
        text="Soup", 
        command=lambda: show_recipes("Soup"),
        width=120,
        height=40,
        corner_radius=10   
    )
    button1.pack(pady=10, padx=10, anchor="w")

    button2 = ctk.CTkButton(
        sidebar_frame, 
        text="Baked", 
        command=lambda: show_recipes("Baked"),
        width=120,
        height=40,
        corner_radius=10
    )
    button2.pack(pady=10, padx=10, anchor="w")

    button3 = ctk.CTkButton(
        sidebar_frame, 
        text="Deep Fried", 
        command=lambda: show_recipes("Fried/Deep Fried"),
        width=120,
        height=40,
        corner_radius=10
    )
    button3.pack(pady=10, padx=10, anchor="w")

    button4 = ctk.CTkButton(
        sidebar_frame, 
        text="Vegetarian", 
        command=lambda: show_recipes("Vegetarian"),
        width=120,
        height=40,
        corner_radius=10
    )
    button4.pack(pady=10, padx=10, anchor="w")
>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88

    # Save recipe button
    save_button = ctk.CTkButton(
<<<<<<< HEAD
        sidebar_frame,
        text="Save Recipe",
        command=lambda: save_recipe(controller),
=======
        sidebar_frame, 
        text="Save", 
        command=save_recipe,
>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88
        width=120,
        height=40,
        corner_radius=10
    )
    save_button.pack(pady=20, padx=10, anchor="w")

<<<<<<< HEAD
    # Back to homepage button
=======
    main_frame = ctk.CTkFrame(main_container, width=600, height=600, corner_radius=10)
    main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Expands to fill available space
    
    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search for recipes...", width=520)
    search_entry.pack(pady=10)

    def on_search_change(event=None):
        search_query = search_entry.get()
        show_recipes(search_query=search_query)

    search_entry.bind("<KeyRelease>", on_search_change)

    recipes_frame = ctk.CTkFrame(main_frame)
    recipes_frame.pack(fill="both", expand=True, padx=20, pady=20)

>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88
    back_button = ctk.CTkButton(
        sidebar_frame,
        text="Back to Homepage",
        command=controller.show_homepage,
        width=120,
        height=40,
        corner_radius=10
    )
    back_button.pack(pady=40, padx=10, anchor="w")

<<<<<<< HEAD
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
=======
def set_selected_recipe(item): 
    global selected_recipe
    selected_recipe = item
    print(f"selected {selected_recipe}") 

def save_recipe():
    global selected_recipe
    if selected_recipe:
        recipe_name = selected_recipe["name"] if isinstance(selected_recipe, dict) else selected_recipe
        saved_recipes.append(recipe_name)
        print(f"saved: {recipe_name}") 
    else:
        print("no recipe selected") 
>>>>>>> b1e78aa5e8521bee1c2494eca600ea1f5ef9ff88
