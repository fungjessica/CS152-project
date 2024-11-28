import json
import os
import customtkinter as ctk
from utilities import clear_window
from recipe_data import saved_recipes
from PIL import Image

def load_recipes():
    file_path = os.path.join(os.path.dirname(__file__), 'recipes.json')
    try:
        with open(file_path, "r") as file:
            recipe_data = json.load(file)
        return recipe_data
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return {}

selected_recipe = None

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

    def show_recipes(category=None, search_query=""):
        global selected_recipe

        for widget in recipes_frame.winfo_children():
            widget.destroy()

        header.configure(text="Recipes")

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

    save_button = ctk.CTkButton(
        sidebar_frame, 
        text="Save", 
        command=save_recipe,
        width=120,
        height=40,
        corner_radius=10
    )
    save_button.pack(pady=20, padx=10, anchor="w")

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

    back_button = ctk.CTkButton(
        sidebar_frame, 
        text="Back to Homepage", 
        command=controller.show_homepage,
        width=120, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 10)
    )
    back_button.pack(padx=10, pady=60)

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
