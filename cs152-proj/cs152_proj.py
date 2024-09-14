#references: 
#https://www.pythonguis.com/tutorials/create-gui-tkinter/

from tkinter import* #python GUI
window = Tk() #create window (root) 

window.title("Grocery To-Do List") #changes window title
window.minsize(400,400)
window.configure(background="pink")

text = Label(window, text="Homepage")
text.pack()
button = Button(window, text="button")
button.pack(side='top')
#leave at bottom! 
window.mainloop() 