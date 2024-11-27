import json
import os
import customtkinter as ctk
from utilities import clear_window
from recipe_data import saved_recipes
from PIL import Image

# Load the recipe data from the JSON file
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
    """Allows users to browse available recipes."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Browse Recipes", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    # Main container frame for the layout
    main_container = ctk.CTkFrame(root)
    main_container.pack(pady=10, padx=10, fill="both", expand=True)

    # Sidebar frame on the left for navigation buttons
    sidebar_frame = ctk.CTkFrame(main_container, width=125, height=600, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    # Prevent sidebar from resizing
    sidebar_frame.grid_propagate(False)
    sidebar_frame.pack_propagate(False)

    # Configure the grid to keep sidebar fixed
    main_container.grid_columnconfigure(0, weight=0, minsize=100)  # Fixed width for sidebar
    main_container.grid_columnconfigure(1, weight=1)  # Main content adjusts to resizing
    main_container.grid_rowconfigure(0, weight=1)  # Allow vertical resizing only for content


    # Load recipe categories from the JSON file
    recipe_data = load_recipes()

    # Function to show recipes based on category or search query
    def show_recipes(category=None, search_query=""):
        global selected_recipe

        # Clear previous recipe buttons
        for widget in recipes_frame.winfo_children():
            widget.destroy()

        header.configure(text="Recipes")

        # Filter recipes based on category and search query
        if category:
            recipes_to_display = recipe_data.get(category, [])
        else:
            recipes_to_display = []
            for category, recipes in recipe_data.items():
                for recipe in recipes:
                    if search_query.lower() in recipe.lower():  # Case insensitive search
                        recipes_to_display.append(recipe)

        # Display the filtered recipes
        for idx, item in enumerate(recipes_to_display):
            row = idx // 4
            column = idx % 4
            image_path = os.path.join(os.path.dirname(__file__), "images", item["image"])
            item_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))  # Adjust size as needed
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

    # Buttons in the sidebar (pass the category names)
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

    # Main frame on the right for the recipe list and search bar
    main_frame = ctk.CTkFrame(main_container, width=600, height=600, corner_radius=10)
    main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Expands to fill available space
    
    # Search bar at the top of the main frame
    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search for recipes...", width=520)
    search_entry.pack(pady=10)

    # Function to update the recipe display based on search query
    def on_search_change(event=None):
        search_query = search_entry.get()
        show_recipes(search_query=search_query)

    search_entry.bind("<KeyRelease>", on_search_change)

    # Frame to display recipe items in the main frame
    recipes_frame = ctk.CTkFrame(main_frame)
    recipes_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Back to homepage button
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

# Function to select the recipe from the grid
def set_selected_recipe(item): 
    global selected_recipe
    selected_recipe = item
    print(f"selected {selected_recipe}") # debug

# Function to save selected recipe to array (see recipe_data.py)
def save_recipe():
    global selected_recipe
    if selected_recipe:
        saved_recipes.append(selected_recipe)
        print(f"saved: {selected_recipe}") # debug
    else:
        print("no recipe selected") # debug
