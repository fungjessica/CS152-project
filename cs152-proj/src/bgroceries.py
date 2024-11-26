import customtkinter as ctk
from utilities import clear_window
from recipe_data import saved_groceries

def browse_groceries(root, controller):
    """Allows users to browse available grocery items."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Browse Groceries", font=("Helvetica", 24, "bold"))
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
    def show_groceries(category, grocery_categories):
        global selected_groceries

        for widget in groceries_frame.winfo_children():
            widget.destroy()

        header.configure(text=f"{category} Groceries")

        for idx, item in enumerate(grocery_categories):
            row = idx // 3  # Calculate the current row
            column = idx % 3  # Calculate the current column (0, 1, 2 for each row)
            # Display item label in the calculated row and column
            item_button = ctk.CTkButton(
                groceries_frame, 
                text=item, 
                font=("Helvetica", 14),
                command=lambda item=item: set_selected_groceries(item),  
                fg_color="transparent",
                border_width=0
            )
            item_button.grid(row=row, column=column, padx=60, pady=60)
    # Buttons in the sidebar
    button1 = ctk.CTkButton(
        sidebar_frame, 
        text="Vegetables", 
        command=lambda: show_groceries("Vegetables", ["Spinach", "Cabbage", "Lettuce", "Carrots",
                                               "Broccoli", "Kale", "Celery", "Bok Choy"]),
        width=120,
        height=40,
        corner_radius=10   
    )
    button1.pack(pady=10, padx=10, anchor="w")

    button2 = ctk.CTkButton(
        sidebar_frame, 
        text="Fruits", 
        command=lambda: show_groceries("Fruits", ["Strawberries", "Apples", "Star Fruit", "Dragon Fruit", "Pineapples", "Watermelon",
                                               "Cantalope", "Wintermelon"]),
        width=120,
        height=40,
        corner_radius=10
    )
    button2.pack(pady=10, padx=10, anchor="w")

    save_button = ctk.CTkButton(
        sidebar_frame, 
        text="Save Groceries", 
        command=save_grocery,
        width=120,
        height=40,
        corner_radius=10
    )
    save_button.pack(pady=20, padx=10, anchor="w")
    # Main frame on the right for the grocery list and search bar
    main_frame = ctk.CTkFrame(main_container, width=600, height=600, corner_radius=10)
    main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Expands to fill available space
    
    # Search bar at the top of the main frame
    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search for groceries...", width=520)
    search_entry.pack(pady=10)

    # Frame to display grocery items in the main frame
    groceries_frame = ctk.CTkFrame(main_frame)
    groceries_frame.pack(fill="both", expand=True, padx=20, pady=20)

    
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

def set_selected_groceries(item): 
    global selected_groceries
    selected_groceries = item
    print(f"selected {selected_groceries}") #debug

#function to save selected recipe to array (see recipe_data.py)
def save_grocery():
    global selected_groceries
    if selected_groceries:
        saved_groceries.append(selected_groceries)
        print(f"saved: {selected_groceries}") #debug
    else:
        print("no groceries selected") #debug
