from tkinter import *
# import filedialog module
from tkinter import filedialog
  
# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/home/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

#Creacion de el frame raiz
root = Tk()

root.title("Simulador SO")

root.resizable(True,True)

root.config(bd=10)

root.config(relief="groove")

#Creacion del frame principal
mainFrame = Frame()

mainFrame.pack(fill="both")

mainFrame.config(width="720",height="650")

#Creacion del titulo del frame
Label(mainFrame, text="Simulador de Algoritmos de paginación",justify="center").grid(row=0, column=1,pady=4)

#Label y contenedor de la entrada de la semilla
seedLabel = Label(mainFrame, text="Semilla")
seedLabel.grid(row=1,column=0, padx=4,pady=4)

seedEntry = Entry(mainFrame)
seedEntry.grid(row=1,column=1, padx=4,pady=4)
seedEntry.config(justify="center")

#Creacion del combobox
algotLabel = Label(mainFrame, text="Algoritmo")
algotLabel.grid(row=2,column=0, padx=4,pady=4)

choices = ["FIFO","SC","MRU","RND"]
selected = StringVar()
selected.set(choices[0])

opmAlgo = OptionMenu(mainFrame, selected, *choices)
opmAlgo.grid(row=2,column=1, padx=4,pady=4)
opmAlgo.config(cursor="hand2")

#Input del archivo a cargar
button_explore = Button(mainFrame,text = "Archivo",command = browseFiles)
button_explore.grid(column = 0, row = 3,padx=4,pady=4)
button_explore.config(cursor="hand2")

label_file_explorer = Label(mainFrame, text = "File Explorer", width = 65, height = 4,fg = "blue")
label_file_explorer.grid(column = 1, row = 3,padx=4)

#Cracion del boton de ejecucion
btnRun = Button(mainFrame,text="Correr")
btnRun.grid(row=4,column=1)
btnRun.config(cursor="hand2")

root.mainloop()

