import customtkinter as ctk

#close the window
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

#toggle between light/dark mode
def toggle_mode(controller):
    if controller.appearance_mode == "dark":
        controller.appearance_mode = "light"
        ctk.set_appearance_mode("light")
        controller.mode_toggle_button.configure(text="Dark Mode")
    else:
        controller.appearance_mode = "dark"
        ctk.set_appearance_mode("dark")
        controller.mode_toggle_button.configure(text="Light Mode")

#close the app
def quit_app(root):
    quit_button = ctk.CTkButton(
        root,
        text="Exit",
        command=root.destroy,  
        width=100,
        height=30,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    quit_button.place(relx=0.95, rely=0.95, anchor="se")