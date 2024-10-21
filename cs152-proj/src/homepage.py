import customtkinter as ctk
from utilities import clear_window, toggle_mode, quit_app

def show_homepage(root, controller):
    """Displays the homepage with navigation options."""
    from utilities import clear_window
    clear_window(root)

    header = ctk.CTkLabel(root, text="Grocery To-Do List", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    # Button to view grocery lists
    view_lists_button = ctk.CTkButton(
        root,
        text="View Lists",
        command=controller.show_view_lists,
        width=250,
        height=50,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    view_lists_button.pack(pady=20)

    # Button to create a new list
    create_list_button = ctk.CTkButton(
        root,
        text="Create a New List",
        command=controller.show_create_list,
        width=250,
        height=50,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    create_list_button.pack(pady=20)

    # Button to view saved recipes
    saved_recipes_button = ctk.CTkButton(
        root,
        text="Saved Recipes",
        command=controller.show_saved_recipes,
        width=250,
        height=50,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    saved_recipes_button.pack(pady=20)

    # Button to browse grocery items
    browse_button = ctk.CTkButton(
        root,
        text="Browse Groceries",
        command=controller.show_browse_groceries,
        width=250,
        height=50,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    browse_button.pack(pady=20)

    # Mode Toggle Button (Bottom Left)
    controller.mode_toggle_button = ctk.CTkButton(
        root,
        text="Switch to Light Mode" if controller.appearance_mode == "dark" else "Switch to Dark Mode",
        command=lambda: toggle_mode(controller),
        width=150,
        height=30,
        corner_radius=10,
        font=("Helvetica", 12)
    )
    controller.mode_toggle_button.place(relx=0.05, rely=0.95, anchor="sw")

    # Make a quit button at the bottom
    quit_app(root)