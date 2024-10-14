#custom tkinter gui from Tom Schimansky
import customtkinter as ctk

#functions to open different windows
def openRecipeWin():
    recipeWindow = ctk.CTkToplevel(homeWindow)

    recipeWindow.title("Saved Recipes")
    recipeWindow.minsize(500,500)
    recipeWindow.transient(homeWindow)

    headerLabel = ctk.CTkLabel(recipeWindow, text="Saved Recipes")
    headerLabel.pack(pady=5)

def openGroceryWindow():
    groceryWindow = ctk.CTkToplevel(homeWindow)

    groceryWindow.title("Saved Groceries")
    groceryWindow.minsize(500,500)
    groceryWindow.transient(homeWindow)

    headerLabel = ctk.CTkLabel(groceryWindow, text="Grocery List")
    headerLabel.pack(pady=5)

homeWindow = ctk.CTk() #create main window

homeWindow.title("Grocery To-Do List") #changes window title
homeWindow.minsize(500,500)

text = ctk.CTkLabel(homeWindow, text="Homepage")
text.pack(pady=5)

#buttons to open different windows
goToRecipeWin = ctk.CTkButton(homeWindow, text="See Saved Recipes", command=openRecipeWin)
goToRecipeWin.pack(side='top')
goToGroceryWin = ctk.CTkButton(homeWindow, text="See Grocery List", command=openGroceryWindow)
goToGroceryWin.pack(pady=10)



#leave at bottom! 
homeWindow.mainloop() 