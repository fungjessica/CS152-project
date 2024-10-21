import customtkinter as ctk
from utilities import clear_window

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

    # Buttons in the sidebar
    button1 = ctk.CTkButton(
        sidebar_frame, 
        text="Grocery 1", 
        width=120,
        height=40,
        corner_radius=10   
    )
    button1.pack(pady=10, padx=10, anchor="w")

    button2 = ctk.CTkButton(
        sidebar_frame, 
        text="Grocery 2", 
        width=120,
        height=40,
        corner_radius=10
    )
    button2.pack(pady=10, padx=10, anchor="w")

    # Main frame on the right for the grocery list and search bar
    main_frame = ctk.CTkFrame(main_container, width=600, height=600, corner_radius=10)
    main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Expands to fill available space
    
    # Search bar at the top of the main frame
    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search for groceries...", width=520)
    search_entry.pack(pady=10)

    # Frame to display grocery items in the main frame
    groceries_frame = ctk.CTkFrame(main_frame)
    groceries_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Example available grocery items
    grocery_items = ["Milk", "Eggs", "Bread", "Butter", "Cheese", "Apples", "Bananas", "Chicken"]

    # Display grocery items in a grid with 3 items per row
    for idx, item in enumerate(grocery_items):
        row = idx // 3  # Calculate the current row
        column = idx % 3  # Calculate the current column (0, 1, 2 for each row)
        
        # Display item label in the calculated row and column
        item_label = ctk.CTkLabel(groceries_frame, text=item, font=("Helvetica", 14))
        item_label.grid(row=row, column=column, padx=60, pady=50)

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
    back_button.pack(padx=10, pady=150)