import customtkinter as ctk
from utilities import clear_window, toggle_mode, quit_app

#function to show the app's homepage
def show_homepage(root, controller):
    from utilities import clear_window
    clear_window(root)

    header = ctk.CTkLabel(root, text="Grocery To-Do List", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    view_lists_button = ctk.CTkButton(
        root,
        text="View Lists",
        command=controller.show_view_lists,
        width=250,
        height=60,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    view_lists_button.pack(pady=20)

    create_list_button = ctk.CTkButton(
        root,
        text="Create a New List",
        command=controller.show_create_list,
        width=250,
        height=60,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    create_list_button.pack(pady=20)

    browse_recipes_button = ctk.CTkButton(
        root, 
        text="Browse Recipes", 
        command=controller.show_browse_recipes,
        width=250,
        height=60,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    browse_recipes_button.pack(pady=20)

    saved_recipes_button = ctk.CTkButton(
        root,
        text="Saved Recipes",
        command=controller.show_saved_recipes,
        width=250,
        height=60,
        corner_radius=10,
        font=("Helvetica", 16)
    )
    saved_recipes_button.pack(pady=20)

    controller.mode_toggle_button = ctk.CTkButton(
        root,
        text="Light Mode" if controller.appearance_mode == "dark" else "Dark Mode",
        command=lambda: toggle_mode(controller),
        width=100,
        height=30,
        corner_radius=10,
        font=("Helvetica", 12)
    )
    controller.mode_toggle_button.place(relx=0.05, rely=0.95, anchor="sw")

    quit_app(root)