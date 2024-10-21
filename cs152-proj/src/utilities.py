import customtkinter as ctk

def clear_window(root):
    """Clears the window by destroying all its child widgets."""
    for widget in root.winfo_children():
        widget.destroy()

def toggle_mode(controller):
    """Switch between dark and light modes."""
    if controller.appearance_mode == "dark":
        controller.appearance_mode = "light"
        ctk.set_appearance_mode("light")
        controller.mode_toggle_button.configure(text="Dark Mode")
    else:
        controller.appearance_mode = "dark"
        ctk.set_appearance_mode("dark")
        controller.mode_toggle_button.configure(text="Light Mode")

def quit_app(root):
    """Creates a button that quits the application."""
    quit_button = ctk.CTkButton(
        root,
        text="Exit",
        command=root.destroy,  # This will close the window and quit the program
        width=100,
        height=30,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    quit_button.place(relx=0.95, rely=0.95, anchor="se")