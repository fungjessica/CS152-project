import os
import json
import customtkinter as ctk
from utilities import clear_window
from bgroceries import load_groceries
from PIL import Image
import tkinter as tk

GROCERY_LISTS_FILE = os.path.join(os.path.dirname(__file__), "grocery_lists.json")

def create_list_flow(root, controller):
    """Flow to enter the grocery list name."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Create a New Grocery List", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    list_name_entry = ctk.CTkEntry(root, width=200,justify="center", placeholder_text="Enter list name")
    list_name_entry.pack(pady=10)

    warning_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12), text_color="red")
    warning_label.pack(pady=10)

    proceed_button = ctk.CTkButton(
        root,
        text="Next: Choose Items",
        command=lambda: validate_list_name(root, controller, list_name_entry, warning_label),
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    proceed_button.pack(pady=10)

    back_button = ctk.CTkButton(
        root, 
        text="Back to Homepage", 
        command=controller.show_homepage, 
        width=150, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

def validate_list_name(root, controller, list_name_entry, warning_label):
    list_name = list_name_entry.get().strip()  

    if not list_name: 
        warning_label.configure(text="List name cannot be blank! Please enter a name.")  

        root.after(2000, lambda: warning_label.configure(text=""))
    else:
        choose_items_flow(root, controller, list_name)

def choose_items_flow(root, controller, list_name):
    clear_window(root)

    header = ctk.CTkLabel(root, text=f"Browse Groceries for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    main_container = ctk.CTkFrame(root)
    main_container.pack(pady=10, padx=10, fill="both", expand=True)

    # Configure grid layout for the main container
    main_container.grid_columnconfigure(0, weight=0, minsize=150)  # Sidebar
    main_container.grid_columnconfigure(1, weight=1)  # Main content
    main_container.grid_rowconfigure(1, weight=1)  # Scrollable frame

    # Sidebar for categories
    sidebar_frame = ctk.CTkFrame(main_container, width=125, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="ns")

    groceries_data = load_groceries()
    selected_items = []

    # Search bar
    search_entry = ctk.CTkEntry(main_container, placeholder_text="Search for groceries...", width=520)
    search_entry.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="ew")

    # Scrollable frame for grocery items
    scrollable_frame = ctk.CTkScrollableFrame(main_container, width=600, corner_radius=10)
    scrollable_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    # Function to filter groceries by search query or category
    def show_groceries(category=None, search_query=""):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if category:
            groceries_to_display = groceries_data.get(category, [])
        else:
            groceries_to_display = []
            for items in groceries_data.values():
                groceries_to_display.extend(items)

        if search_query:
            search_query = search_query.lower()
            groceries_to_display = [
                item for item in groceries_to_display if search_query in item["name"].lower()
            ]

        for idx, item in enumerate(groceries_to_display):
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

    # Function to toggle item selection
    def toggle_selection(item_name, button):
        if item_name in selected_items:
            selected_items.remove(item_name)
            button.configure(fg_color="transparent")  # Deselect
        else:
            selected_items.append(item_name)
            button.configure(fg_color="#3b82f6")  # Highlight as selected
        update_proceed_button_state()

    # Update the state of the proceed button
    def update_proceed_button_state():
        if selected_items:
            proceed_button.configure(state="normal", fg_color="#3b82f6")
        else:
            proceed_button.configure(state="disabled", fg_color="#a0a0a0")

    # Enable real-time search functionality
    def on_search_change(event=None):
        search_query = search_entry.get()
        show_groceries(search_query=search_query)

    search_entry.bind("<KeyRelease>", on_search_change)

    # All button to show all ingredients
    all_button = ctk.CTkButton(
        sidebar_frame,
        text="All",
        command=lambda: show_groceries(),
        width=120,
        height=40,
        corner_radius=10
    )
    all_button.pack(pady=(10, 10), padx=10, anchor="w")

    # Sidebar buttons for categories
    for category in groceries_data.keys():
        category_button = ctk.CTkButton(
            sidebar_frame,
            text=category,
            command=lambda cat=category: show_groceries(cat),
            width=120,
            height=40,
            corner_radius=10
        )
        category_button.pack(pady=10, padx=10, anchor="w")

    # Add Next and Back buttons
    proceed_button = ctk.CTkButton(
        sidebar_frame,
        text="Next",
        command=lambda: proceed_to_quantities(),
        width=120,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14),
        state="disabled",  # Initially disabled
        fg_color="#EBEBE4",  # Greyed out
        text_color="#ffffff",  # Text color
    )
    proceed_button.pack(pady=(60, 10))

    back_button = ctk.CTkButton(
        sidebar_frame,
        text="Back",
        command=lambda: create_list_flow(root, controller),
        width=120,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

    # Function to proceed to quantity selection
    def proceed_to_quantities():
        if selected_items:
            selected_items_dict = {item: {"selected": True, "quantity": None} for item in selected_items}
            set_quantities_flow(root, controller, list_name, selected_items_dict)

    # Show all groceries by default
    show_groceries()

def set_quantities_flow(root, controller, list_name, selected_items):
    clear_window(root)

    # Header
    header = ctk.CTkLabel(root, text=f"Set Quantities for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    # Scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(root, width=600, height=300, corner_radius=10)
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    title_frame = ctk.CTkFrame(scrollable_frame)
    title_frame.pack(fill="x", pady=(0, 10))

    title_frame.grid_columnconfigure(0, weight=1)  # Item title column
    title_frame.grid_columnconfigure(1, weight=0)  # Quantity title column

    item_title = ctk.CTkLabel(title_frame, text="Items", font=("Helvetica", 16, "bold"))
    item_title.grid(row=0, column=0, padx=20, sticky="w")

    quantity_title = ctk.CTkLabel(title_frame, text="Quantity", font=("Helvetica", 16, "bold"))
    quantity_title.grid(row=0, column=1, padx=55, sticky="e")

    # Add items to the scrollable frame
    for idx, (item, data) in enumerate(selected_items.items()):
        if data["selected"]:  # Only include selected items
            item_frame = ctk.CTkFrame(scrollable_frame)
            item_frame.pack(padx=5, pady=5, fill="x")

            item_frame.grid_columnconfigure(0, weight=1)  # Item name column
            item_frame.grid_columnconfigure(1, weight=0)  # Quantity column

            # Item name
            item_label = ctk.CTkLabel(item_frame, text=item, font=("Helvetica", 14))
            item_label.grid(row=0, column=0, padx=10, sticky="w")

            # Quantity controls
            quantity_frame = ctk.CTkFrame(item_frame)
            quantity_frame.grid(row=0, column=1, padx=20, sticky="e")

            minus_button = ctk.CTkButton(
                quantity_frame, text="-", width=30,
                command=lambda i=item: decrease_quantity(i, selected_items)
            )
            minus_button.pack(side="left")

            quantity_var = tk.IntVar(value=1 if data.get("quantity", 1) is None else data["quantity"])
            data["quantity"] = quantity_var

            quantity_entry = ctk.CTkEntry(quantity_frame, textvariable=quantity_var, width=50, justify="center")
            quantity_entry.pack(side="left", padx=5)

            plus_button = ctk.CTkButton(
                quantity_frame, text="+", width=30,
                command=lambda i=item: increase_quantity(i, selected_items)
            )
            plus_button.pack(side="left")

    # Create list button
    create_button = ctk.CTkButton(
        root, 
        text="Create List", 
        command=lambda: create_list(root, controller, list_name, selected_items), 
        width=200, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    create_button.pack(pady=20)

    # Back button
    back_button = ctk.CTkButton(
        root, 
        text="Back to Item Selection", 
        command=lambda: choose_items_flow(root, controller, list_name),  
        width=150, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

def increase_quantity(item_name, selected_items):
    current_qty = selected_items[item_name]["quantity"].get()
    selected_items[item_name]["quantity"].set(current_qty + 1)

def decrease_quantity(item_name, selected_items):
    current_qty = selected_items[item_name]["quantity"].get()
    if current_qty > 1:  # Ensure the quantity doesn't go below 1
        selected_items[item_name]["quantity"].set(current_qty - 1)

def create_list(root, controller, list_name, selected_items):
    try:
        # Validate quantities
        for item, data in selected_items.items():
            if data["selected"] and (data["quantity"] is None or data["quantity"] <= 0):
                raise ValueError("Invalid quantity")

        # Save the list
        grocery_list = {
            item: {"quantity": data["quantity"]} for item, data in selected_items.items() if data["selected"]
        }
        controller.grocery_lists[list_name] = grocery_list
        save_grocery_lists_to_file(controller.grocery_lists)

        # Show the view lists screen
        controller.show_view_lists()

    except ValueError:
        # Show error label
        error_label = ctk.CTkLabel(
            root,
            text="Error: Please ensure all selected items have a valid quantity.",
            font=("Helvetica", 12),
            text_color="red"
        )
        error_label.pack(pady=10)


def load_grocery_lists():
    if os.path.exists(GROCERY_LISTS_FILE):
        try:
            with open(GROCERY_LISTS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading grocery lists file.")
            return {}
    return {}

def save_grocery_lists_to_file(lists):
    with open(GROCERY_LISTS_FILE, "w") as file:
        json.dump(lists, file, indent=4)

def create_list(root, controller, list_name, selected_items):
    try:
        # Validate quantities
        for item, data in selected_items.items():
            if data["selected"] and (data["quantity"] is None or data["quantity"].get() <= 0):
                raise ValueError("Invalid quantity")

        # Save the list
        grocery_list = {
            item: {"quantity": data["quantity"].get()} for item, data in selected_items.items() if data["selected"]
        }
        controller.grocery_lists[list_name] = grocery_list
        save_grocery_lists_to_file(controller.grocery_lists)

        # Show the view lists screen
        controller.show_view_lists()

    except ValueError:
        # Show error label
        error_label = ctk.CTkLabel(
            root,
            text="Error: Please ensure all selected items have a valid quantity.",
            font=("Helvetica", 12),
            text_color="red"  # Corrected from fg="red"
        )
        error_label.pack(pady=10)

