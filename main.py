from tkinter import *
# import filedialog module
from tkinter import filedialog

#ttk import
from tkinter import ttk

import random

#Variables globales
filename = ""
fileSelected=False


# Function for opening the
# file explorer window
def browseFiles():
    global filename
    global fileSelected
    filename = filedialog.askopenfilename(initialdir = "/home/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
    fileSelected=True
    # Cambio de la etiqueta Archivo
    label_file_explorer.configure(text="File Opened: "+filename)


def printSelectedOp():
    global filename
    print(selected.get())
    print(seedEntry.get())
    print(filename)


def fileGenerator(seed, p, n):
    random.seed(seed)
    procesList = {}
    comdList = []
    killProcess = []
    ptrCount = 1
    comandList = ["new", "use", "delete", "kill"]
    weights = [0.3, 0.6, 0.05, 0.05]

    i = 1
    while i <= n and len(killProcess) != p:
        chs = random.choices(comandList,weights)[0]
        if chs == "new":
            rndPID = random.randint(1, p)
            if rndPID not in killProcess:
                procesList[rndPID] = ptrCount
                comdList.append(comandList[0] + "(" + str(rndPID) + "," + str(random.randint(50, 1000)) + ")\n")
                ptrCount += 1
                i += 1

        if chs == "use" and len(procesList) != 0:
            procesListAux = []
            procesListAux.extend(procesList.values())
            randPtr = random.choice(procesListAux)
            comdList.append(comandList[1] + "(" + str(randPtr) + ")\n")
            i += 1

        if chs == "delete" and len(procesList) != 0:
            procesListAux = []
            procesListAux.extend(procesList.values())
            randPtr = random.choice(procesListAux)
            comdList.append(comandList[2] + "(" + str(randPtr) + ")\n")
            procesList = {key: value for key, value in procesList.items() if value != randPtr}
            i += 1

        if chs == "kill" and len(procesList) != 0:
            procesListAux = []
            procesListAux.extend(procesList.keys())
            randPID = random.choice(procesListAux)
            comdList.append(comandList[3] + "(" + str(randPID) + ")\n")
            procesList = {key: value for key, value in procesList.items() if key != randPID}
            killProcess.append(randPID)
            i += 1

        print(chs)
        print(i)

    print(procesList)
    print(comdList)
    # Open a file for writing
    with open('generatedFile.txt', 'w') as f:
        # Write some text to the file
        for i in comdList:
            f.write(i)


#Creacion de la nueva ventana
def openNewWindow():
    fileGenerator(seedEntry.get(), int(pselected.get()), int(opselected.get()))
    #fileGenerator(0,10,176)
    newWindow = Toplevel(root)
    newWindow.title("Ejecuntando")
    
    global selected
   

    #Creacion del mainframe de a la ventana emergente 

    nwMainFrame = Frame(newWindow)

    nwMainFrame.pack(fill="both")

    nwMainFrame.config(width="720",height="650")
    
    #Tabla del OPT
    Label(nwMainFrame, text="MMU-OPT" ,justify="center").grid(row=0, column=0)
    
    h = Scrollbar(nwMainFrame, orient='vertical')

    tv = ttk.Treeview(nwMainFrame,yscrollcommand=h.set, columns=("col1","col2","col3","col4","col5","col6","col7"))
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
    tv.grid(row=1,column=0)

    h.configure(command=tv.yview)
    h.grid(row=1,column=1,rowspan=1,sticky=NS)
 

    #Inferior
    tvi1 = ttk.Treeview(nwMainFrame, columns=("col1"))
    tvi1.column("#0",width=70)
    tvi1.column("col1",width=70,anchor=CENTER)
   
    
    tvi1.heading("#0",text="Processes", anchor=CENTER)
    tvi1.heading("col1",text="Sim-Time",anchor=CENTER)
   
    tvi1.grid(row=2,column=0)


    tvi2 = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3"))
    tvi2.column("#0",width=70)
    tvi2.column("col1",width=70,anchor=CENTER)
    tvi2.column("col2",width=70,anchor=CENTER)
    tvi2.column("col3",width=70,anchor=CENTER)
    
    
    tvi2.heading("#0",text="RAM KB", anchor=CENTER)
    tvi2.heading("col1",text="RAM %",anchor=CENTER)
    tvi2.heading("col2",text="V-RAM KB",anchor=CENTER)
    tvi2.heading("col3",text="V-RAM %",anchor=CENTER)
    
    tvi2.grid(row=3,column=0)


    tvi3 = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3","col4"))
    tvi3.column("#0",width=70)
    tvi3.column("col1",width=70,anchor=CENTER)
    tvi3.column("col2",width=70,anchor=CENTER)
    tvi3.column("col3",width=70,anchor=CENTER)
    tvi3.column("col4",width=70,anchor=CENTER)
    
    
    tvi3.heading("#0",text="P-LOADED", anchor=CENTER)
    tvi3.heading("col1",text="P-UNLOADED",anchor=CENTER)
    tvi3.heading("col2",text="Trashing-s",anchor=CENTER)
    tvi3.heading("col3",text="Trashing-%",anchor=CENTER)
    tvi3.heading("col4",text="Fragmentación",anchor=CENTER)
    
    tvi3.grid(row=4,column=0)



    #------------------------------------------------------------------------------

    #Tabla del algoritmo a comparar

    h2 = Scrollbar(nwMainFrame, orient='vertical')

    Label(nwMainFrame, text="MMU-" + selected.get(),justify="center").grid(row=0, column=2)

    tv1 = ttk.Treeview(nwMainFrame,yscrollcommand=h2.set, columns=("col1","col2","col3","col4","col5","col6","col7"))
    tv1.column("#0",width=70)
    tv1.column("col1",width=70,anchor=CENTER)
    tv1.column("col2",width=70,anchor=CENTER)
    tv1.column("col3",width=70,anchor=CENTER)
    tv1.column("col4",width=70,anchor=CENTER)
    tv1.column("col5",width=70,anchor=CENTER)
    tv1.column("col6",width=70,anchor=CENTER)
    tv1.column("col7",width=70,anchor=CENTER)
    
    tv1.heading("#0",text="PAGE ID", anchor=CENTER)
    tv1.heading("col1",text="PID",anchor=CENTER)
    tv1.heading("col2",text="LOADED",anchor=CENTER)
    tv1.heading("col3",text="L-ADDR",anchor=CENTER)
    tv1.heading("col4",text="M-ADDR",anchor=CENTER)
    tv1.heading("col5",text="D-ADDR",anchor=CENTER)
    tv1.heading("col6",text="LOADED-T",anchor=CENTER)
    tv1.heading("col7",text="MARK",anchor=CENTER) 
    tv1.grid(row=1,column=2)
   
    h2.configure(command=tv1.yview)
    h2.grid(row=1,column=3,rowspan=1,sticky=NS)

     #Inferior
    tv1i1 = ttk.Treeview(nwMainFrame, columns=("col1"))
    tv1i1.column("#0",width=70)
    tv1i1.column("col1",width=70,anchor=CENTER)
   
    
    tv1i1.heading("#0",text="Processes", anchor=CENTER)
    tv1i1.heading("col1",text="Sim-Time",anchor=CENTER)
   
    tv1i1.grid(row=2,column=2)


    tv1i2 = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3"))
    tv1i2.column("#0",width=70)
    tv1i2.column("col1",width=70,anchor=CENTER)
    tv1i2.column("col2",width=70,anchor=CENTER)
    tv1i2.column("col3",width=70,anchor=CENTER)
    
    
    tv1i2.heading("#0",text="RAM KB", anchor=CENTER)
    tv1i2.heading("col1",text="RAM %",anchor=CENTER)
    tv1i2.heading("col2",text="V-RAM KB",anchor=CENTER)
    tv1i2.heading("col3",text="V-RAM %",anchor=CENTER)
    
    tv1i2.grid(row=3,column=2)


    tv1i3 = ttk.Treeview(nwMainFrame, columns=("col1","col2","col3","col4"))
    tv1i3.column("#0",width=70)
    tv1i3.column("col1",width=70,anchor=CENTER)
    tv1i3.column("col2",width=70,anchor=CENTER)
    tv1i3.column("col3",width=70,anchor=CENTER)
    tv1i3.column("col4",width=70,anchor=CENTER)
    
    
    tv1i3.heading("#0",text="P-LOADED", anchor=CENTER)
    tv1i3.heading("col1",text="P-UNLOADED",anchor=CENTER)
    tv1i3.heading("col2",text="Trashing-s",anchor=CENTER)
    tv1i3.heading("col3",text="Trashing-%",anchor=CENTER)
    tv1i3.heading("col4",text="Fragmentación",anchor=CENTER)
    
    tv1i3.grid(row=4,column=2)


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

#Creacion del combobox Algoritmo
algotLabel = Label(mainFrame, text="Algoritmo")
algotLabel.grid(row=2,column=0, padx=4,pady=4)

choices = ["FIFO","SC","MRU","RND"]
selected = StringVar(mainFrame)
selected.set(choices[0])

opmAlgo = OptionMenu(mainFrame, selected, *choices)
opmAlgo.grid(row=2,column=1, padx=4,pady=4)
opmAlgo.config(cursor="hand2")

#Creacion del combobox N procesos
pLabel = Label(mainFrame, text="Numero de procesos")
pLabel.grid(row=3,column=0,pady=4)

pchoices = ["10","50","100"]
pselected = StringVar(mainFrame)
pselected.set(pchoices[0])

opmp = OptionMenu(mainFrame, pselected, *pchoices)
opmp.grid(row=3,column=1,pady=4)
opmp.config(cursor="hand2")

#Creacion del combobox N operaciones
opLabel = Label(mainFrame, text="Numero de operaciones")
opLabel.grid(row=3,column=2,pady=4)

opchoices = ["500","1000","5000"]
opselected = StringVar(mainFrame)
opselected.set(opchoices[0])

opmAlgo = OptionMenu(mainFrame, opselected, *opchoices)
opmAlgo.grid(row=3,column=3,pady=4)
opmAlgo.config(cursor="hand2")

#Input del archivo a cargar
button_explore = Button(mainFrame,text = "Archivo",command = browseFiles)
button_explore.grid(column = 0, row = 4,padx=4,pady=4)
button_explore.config(cursor="hand2")

label_file_explorer = Label(mainFrame, text = "File Explorer", width = 65, height = 4,fg = "blue")
label_file_explorer.grid(column = 1, row = 4,padx=4)

#Cracion del boton de ejecucion
btnRun = Button(mainFrame,text="Correr", command =  openNewWindow )
btnRun.grid(row=5,column=1)
btnRun.config(cursor="hand2")

root.mainloop()

