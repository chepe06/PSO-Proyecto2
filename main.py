from tkinter import *
# import filedialog module
from tkinter import filedialog

#ttk import
from tkinter import ttk
  
#Variables globales
filename = ""

# Function for opening the
# file explorer window
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/home/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
      
    # Cambio de la etiqueta Archivo
    label_file_explorer.configure(text="File Opened: "+filename)


def printSelectedOp():
    global filename
    print(selected.get())
    print(seedEntry.get())
    print(filename)

#Creacion de la nueva ventana
def openNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("Ejecuntando")
    
    global selected

    #Creacion del mainframe de ala ventana emergente
    nwMainFrame = Frame(newWindow)

    nwMainFrame.pack(fill="both")

    nwMainFrame.config(width="720",height="650")
    
    #Tabla del OPT
    Label(nwMainFrame, text="MMU-OPT" ,justify="center").grid(row=0, column=0,pady=4)

    tv = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3","col4","col5","col6","col7"))
    tv.column("#0",width=70)
    tv.column("col1",width=70,anchor=CENTER)
    tv.column("col2",width=70,anchor=CENTER)
    tv.column("col3",width=70,anchor=CENTER)
    tv.column("col4",width=70,anchor=CENTER)
    tv.column("col5",width=70,anchor=CENTER)
    tv.column("col6",width=70,anchor=CENTER)
    tv.column("col7",width=70,anchor=CENTER)
    
    tv.heading("#0",text="PAGE ID", anchor=CENTER)
    tv.heading("col1",text="PID",anchor=CENTER)
    tv.heading("col2",text="LOADED",anchor=CENTER)
    tv.heading("col3",text="L-ADDR",anchor=CENTER)
    tv.heading("col4",text="M-ADDR",anchor=CENTER)
    tv.heading("col5",text="D-ADDR",anchor=CENTER)
    tv.heading("col6",text="LOADED-T",anchor=CENTER)
    tv.heading("col7",text="MARK",anchor=CENTER) 
    tv.grid(row=1,column=0,pady=10)

    #Tabla del algoritmo a comparar
    Label(nwMainFrame, text="MMU-" + selected.get(),justify="center").grid(row=0, column=1,pady=4)

    tv = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3","col4","col5","col6","col7"))
    tv.column("#0",width=70)
    tv.column("col1",width=70,anchor=CENTER)
    tv.column("col2",width=70,anchor=CENTER)
    tv.column("col3",width=70,anchor=CENTER)
    tv.column("col4",width=70,anchor=CENTER)
    tv.column("col5",width=70,anchor=CENTER)
    tv.column("col6",width=70,anchor=CENTER)
    tv.column("col7",width=70,anchor=CENTER)
    
    tv.heading("#0",text="PAGE ID", anchor=CENTER)
    tv.heading("col1",text="PID",anchor=CENTER)
    tv.heading("col2",text="LOADED",anchor=CENTER)
    tv.heading("col3",text="L-ADDR",anchor=CENTER)
    tv.heading("col4",text="M-ADDR",anchor=CENTER)
    tv.heading("col5",text="D-ADDR",anchor=CENTER)
    tv.heading("col6",text="LOADED-T",anchor=CENTER)
    tv.heading("col7",text="MARK",anchor=CENTER) 
    tv.grid(row=1,column=1,pady=10)



#Creacion del frame raiz
root = Tk()

root.title("Simulador SO")

root.resizable(True,True)

root.config(bd=10)

root.config(relief="groove")

#Creacion del frame principal
mainFrame = Frame(root)

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
selected = StringVar(mainFrame)
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
btnRun = Button(mainFrame,text="Correr", command =  openNewWindow )
btnRun.grid(row=4,column=1)
btnRun.config(cursor="hand2")

root.mainloop()

