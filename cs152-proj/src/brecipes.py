import json
import os
import customtkinter as ctk
from utilities import clear_window
from PIL import Image

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

def save_recipe():
    global selected_recipe
    if selected_recipe:
        recipe_name = selected_recipe["name"] if isinstance(selected_recipe, dict) else selected_recipe
        if recipe_name not in saved_recipes:  # Prevent duplicates
            saved_recipes.append(recipe_name)
            save_recipes_to_file(saved_recipes)  # Persist the data
            print(f"Saved: {recipe_name}")
        else:
            print("Recipe already saved!")
    else:
        print("No recipe selected")

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

    # Configure grid layout
    main_container.grid_columnconfigure(0, weight=0, minsize=150)  # Sidebar
    main_container.grid_columnconfigure(1, weight=1)  # Main content
    main_container.grid_rowconfigure(1, weight=1)  # Scrollable frame

    sidebar_frame = ctk.CTkFrame(main_container, width=125, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="ns")

    recipe_data = load_recipes()
    selected_items = []  # Stores the names of selected recipes

    # Search bar
    search_entry = ctk.CTkEntry(main_container, placeholder_text="Search for recipes...", width=520)
    search_entry.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="ew")

    # Scrollable frame for recipes
    scrollable_frame = ctk.CTkScrollableFrame(main_container, width=600, corner_radius=10)
    scrollable_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def show_recipes(category=None, search_query=""):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if category:
            recipes_to_display = recipe_data.get(category, [])
        else:
            recipes_to_display = []
            for items in recipe_data.values():
                recipes_to_display.extend(items)

        if search_query:
            search_query = search_query.lower()
            recipes_to_display = [
                item for item in recipes_to_display if search_query in item["name"].lower()
            ]

        for idx, item in enumerate(recipes_to_display):
            image_path = os.path.join(os.path.dirname(__file__), "images", item["image"])
            item_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))

            fg_color = "#3b82f6" if item["name"] in selected_items else "transparent"

            def create_button_callback(item_name, button):
                return lambda: toggle_selection(item_name, button)

            item_button = ctk.CTkButton(
                scrollable_frame,
                text=item["name"],
                image=item_image,
                compound="top",
                font=("Helvetica", 14),
                fg_color=fg_color,
                hover_color="#e0e0e0",
            )
            item_button.configure(command=create_button_callback(item["name"], item_button))
            item_button.grid(row=idx // 3, column=idx % 3, padx=30, pady=20)

    def toggle_selection(item_name, button):
        if item_name in selected_items:
            selected_items.remove(item_name)
            button.configure(fg_color="transparent")  # Deselect
        else:
            selected_items.append(item_name)
            button.configure(fg_color="#3b82f6")  # Highlight as selected

    def save_selected_recipes():
        global saved_recipes
        for recipe in selected_items:
            if recipe not in saved_recipes:
                saved_recipes.append(recipe)
        save_recipes_to_file(saved_recipes)

        # Reset the selection
        selected_items.clear()

        # Refresh the display to reset button states
        show_recipes()

    # Real-time search functionality
    def on_search_change(event=None):
        search_query = search_entry.get()
        show_recipes(search_query=search_query)

    search_entry.bind("<KeyRelease>", on_search_change)

    # All button to show all recipes
    all_button = ctk.CTkButton(
        sidebar_frame,
        text="All",
        command=lambda: show_recipes(),
        width=120,
        height=40,
        corner_radius=10
    )
    all_button.pack(pady=(10, 10), padx=10, anchor="w")

    # Sidebar buttons for categories
    for category in recipe_data.keys():
        category_button = ctk.CTkButton(
            sidebar_frame,
            text=category,
            command=lambda cat=category: show_recipes(cat),
            width=120,
            height=40,
            corner_radius=10
        )
        category_button.pack(pady=10, padx=10, anchor="w")


    # Save button
    save_button = ctk.CTkButton(
        sidebar_frame,
        text="Save",
        command=save_selected_recipes,
        width=120,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    save_button.pack(pady=(60, 10))

    # Back button
    back_button = ctk.CTkButton(
        sidebar_frame,
        text="Back",
        command=controller.show_homepage,
        width=120,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

    # Show all recipes by default
    show_recipes()