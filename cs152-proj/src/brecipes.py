import json
import os
import customtkinter as ctk
from utilities import clear_window
from recipe_data import saved_recipes

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

    # Adjust the grid weights to control how much space each frame takes
    main_container.grid_columnconfigure(0, weight=1)  # Sidebar
    main_container.grid_columnconfigure(1, weight=3)  # Main content frame (higher weight = takes more space)
    main_container.grid_rowconfigure(0, weight=1)     # Makes both frames expand vertically

    # Sidebar frame on the left for navigation buttons
    sidebar_frame = ctk.CTkFrame(main_container, width=200, height=600, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    # Load recipe categories from the JSON file
    recipe_data = load_recipes()

    def show_recipes(category):
        global selected_recipe

        for widget in recipes_frame.winfo_children():
            widget.destroy()

        header.configure(text=f"{category} Recipes")

        # Display the recipe items in the `recipes_frame`
        if category in recipe_data:
            recipe_categories = recipe_data[category]
            for idx, item in enumerate(recipe_categories):
                row = idx // 3  # Calculate the current row
                column = idx % 3  # Calculate the current column (0, 1, 2 for each row)
                # Display item label in the calculated row and column
                item_button = ctk.CTkButton(
                    recipes_frame, 
                    text=item, 
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
        text="Fried/Deep Fried", 
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
        text="Save Recipe", 
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

    # Frame to display grocery items in the main frame
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
