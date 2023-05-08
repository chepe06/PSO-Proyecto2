import random
import time
import threading

from tkinter import *
# import filedialog module
from tkinter import filedialog

# ttk import
from tkinter import ttk

from RAM import RAM
from Disk import Disk
from MMU_OPT import MMU_OPT
from MMU_RND import MMU_RND
from MMU_FIFO import MMU_FIFO
from MMU_SC import MMU_SC
from MMU_MRU import MMU_MRU

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
paused = False
filename = ""
fileSelected = False
canvas = ""
canvas1 = ""

# COMPUTER
TOTAL_RAM = 400000
AMOUNT_PAGES = 100
PAGE_SIZE = 4000

#Genera una lista de colores hexadecimales random
def generate_colors():
    colores = []
    if fileSelected:
        for _ in range(1000):
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            colores.append(color)
    else:
        for _ in range(int(pselected.get())+1):
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            colores.append(color)

    return colores

def open_document(filename):
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            instruction = line.split("(")
            if instruction[0] == "new":
                data = instruction[1].split(",")
                instruction[1] = data[0]
                if data[1][-1] == "\n":
                    instruction.append(data[1][:-2])
                else:
                    instruction.append(data[1][:-1])
            elif instruction[0] == "use" or instruction[0] == "delete" or instruction[0] == "kill":
                if instruction[1][-1] == "\n":
                    instruction[1] = instruction[1][:-2]
                else:
                    instruction[1] = instruction[1][:-1]
            instructions.append(instruction)

    return instructions


# Function for opening the
# file explorer window
def browseFiles():
    global filename
    global fileSelected
    filename = filedialog.askopenfilename(initialdir="/home/", title="Select a File",
                                          filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    fileSelected = True
    # Cambio de la etiqueta Archivo
    label_file_explorer.configure(text="File Opened: " + filename)

#Funcion para ver que entradas recibe la interfaz
def printSelectedOp():
    global filename
    print(selected.get())
    print(seedEntry.get())
    print(filename)

#Funcion que genera comando random cuando no se ingresa ningun archivo
def fileGenerator(seed, p, n):
    random.seed(seed)
    procesList = {}
    comdList = []
    killProcess = []
    ptrCount = 1
    comandList = ["new", "use", "delete", "kill"]
    weights = [0.54, 0.44, 0.01, 0.01]  #Pesos para la seleccion random de la lista anterior

    i = 1
    while i <= n and len(killProcess) != p:
        chs = random.choices(comandList, weights)[0]
        if chs == "new":
            rndPID = random.randint(1, p)
            if rndPID not in killProcess:
                procesList[rndPID] = ptrCount
                comdList.append(comandList[0] + "(" + str(rndPID) + "," + str(random.randint(1000, 20000)) + ")\n")
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

        # print(chs)
        # print(i)

    # print(procesList)
    # print(comdList)
    # Open a file for writing
    with open('generatedFile.txt', 'w') as f:
        # Write some text to the file
        for i in comdList:
            f.write(i)


# Creacion de la nueva ventana
def openNewWindow():
    global canvas,canvas1
    newWindow = Toplevel(root)
    newWindow.title("Ejecuntando")

    # Creacion del mainframe de a la ventana emergente

    nwMainFrame = Frame(newWindow)

    nwMainFrame.pack(fill="both")

    nwMainFrame.config(width="720", height="650")

    # Ram del OTP

    Label(nwMainFrame, text="RAM-OTP", justify="center").grid(row=0, column=0)
    # Create a Figure object
    fig = Figure(figsize=(6, 1), dpi=100)

    # Create a table
    table_data = [[]]
    for i in range(100):
        table_data[0].append(" ")
    table = fig.add_subplot(111)
    table.axis('off')  # Hide the axes
    table.axis('tight')
    table.table(cellText=table_data, loc='center')

    # Create a Tkinter canvas that can display the figure
    canvas = FigureCanvasTkAgg(fig, master=nwMainFrame)
    canvas.draw()

    # Pack the canvas into the tkinter window
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=1)

    # Tabla del OPT
    Label(nwMainFrame, text="MMU-OPT", justify="center").grid(row=2, column=0)

    global tv
    h = Scrollbar(nwMainFrame, orient='vertical')

    tv = ttk.Treeview(nwMainFrame, yscrollcommand=h.set, height=8,
                      columns=("col0", "col1", "col2", "col3", "col4", "col5", "col6", "col7"))
    tv.column("#0", width=70)
    tv.column("col0", width=70, anchor=CENTER)
    tv.column("col1", width=70, anchor=CENTER)
    tv.column("col2", width=70, anchor=CENTER)
    tv.column("col3", width=70, anchor=CENTER)
    tv.column("col4", width=70, anchor=CENTER)
    tv.column("col5", width=70, anchor=CENTER)
    tv.column("col6", width=70, anchor=CENTER)
    tv.column("col7", width=70, anchor=CENTER)

    tv.heading("#0", text="INDEX", anchor=CENTER)
    tv.heading("col0", text="PAGE ID", anchor=CENTER)
    tv.heading("col1", text="PID", anchor=CENTER)
    tv.heading("col2", text="LOADED", anchor=CENTER)
    tv.heading("col3", text="L-ADDR", anchor=CENTER)
    tv.heading("col4", text="M-ADDR", anchor=CENTER)
    tv.heading("col5", text="D-ADDR", anchor=CENTER)
    tv.heading("col6", text="LOADED-T", anchor=CENTER)
    tv.heading("col7", text="-----", anchor=CENTER)
    tv.grid(row=3, column=0, pady=5)

    h.configure(command=tv.yview)
    h.grid(row=3, column=1, rowspan=1, sticky=NS)

    # Inferior
    tvi1 = ttk.Treeview(nwMainFrame, height=1, columns=("col1"))
    tvi1.column("#0", width=70)
    tvi1.column("col1", width=70, anchor=CENTER)

    tvi1.heading("#0", text="Processes", anchor=CENTER)
    tvi1.heading("col1", text="Sim-Time", anchor=CENTER)

    tvi1.grid(row=4, column=0, pady=5)

    tvi2 = ttk.Treeview(nwMainFrame, height=1, columns=("col1", "col2", "col3"))
    tvi2.column("#0", width=70)
    tvi2.column("col1", width=70, anchor=CENTER)
    tvi2.column("col2", width=70, anchor=CENTER)
    tvi2.column("col3", width=70, anchor=CENTER)

    tvi2.heading("#0", text="RAM KB", anchor=CENTER)
    tvi2.heading("col1", text="RAM %", anchor=CENTER)
    tvi2.heading("col2", text="V-RAM KB", anchor=CENTER)
    tvi2.heading("col3", text="V-RAM %", anchor=CENTER)

    tvi2.grid(row=5, column=0, pady=5)

    tvi3 = ttk.Treeview(nwMainFrame, height=1, columns=("col1", "col2", "col3", "col4"))
    tvi3.column("#0", width=75)
    tvi3.column("col1", width=75, anchor=CENTER)
    tvi3.column("col2", width=75, anchor=CENTER)
    tvi3.column("col3", width=75, anchor=CENTER)
    tvi3.column("col4", width=75, anchor=CENTER)

    tvi3.heading("#0", text="P-LOADED", anchor=CENTER)
    tvi3.heading("col1", text="P-UNLOADED", anchor=CENTER)
    tvi3.heading("col2", text="Trashing-s", anchor=CENTER)
    tvi3.heading("col3", text="Trashing-%", anchor=CENTER)
    tvi3.heading("col4", text="Fragmentación", anchor=CENTER)

    tvi3.grid(row=6, column=0, pady=5)

    # ------------------------------------------------------------------------------
    # Ram del Algoritmo a comparar
    Label(nwMainFrame, text="RAM-" + selected.get(), justify="center").grid(row=0, column=2)

    # Create a Figure object
    fig1 = Figure(figsize=(6, 1), dpi=100)

    # Create a table
    table_data1 = [[]]
    for i in range(100):
        table_data1[0].append(" ")
    table1 = fig1.add_subplot(111)
    table1.axis('off')  # Hide the axes
    table1.axis('tight')
    table1.table(cellText=table_data1, loc='center')

    # Create a Tkinter canvas that can display the figure
    canvas1 = FigureCanvasTkAgg(fig1, master=nwMainFrame)
    canvas1.draw()

    # Pack the canvas into the tkinter window
    canvas1.get_tk_widget().grid(row=1, column=2, columnspan=1)

    # Tabla del algoritmo a comparar

    h2 = Scrollbar(nwMainFrame, orient='vertical')

    Label(nwMainFrame, text="MMU-" + selected.get(), justify="center").grid(row=2, column=2)

    tv1 = ttk.Treeview(nwMainFrame, yscrollcommand=h2.set, height=8,
                       columns=("col0", "col1", "col2", "col3", "col4", "col5", "col6", "col7"))
    tv1.column("#0", width=70)
    tv1.column("col0", width=70, anchor=CENTER)
    tv1.column("col1", width=70, anchor=CENTER)
    tv1.column("col2", width=70, anchor=CENTER)
    tv1.column("col3", width=70, anchor=CENTER)
    tv1.column("col4", width=70, anchor=CENTER)
    tv1.column("col5", width=70, anchor=CENTER)
    tv1.column("col6", width=70, anchor=CENTER)
    tv1.column("col7", width=70, anchor=CENTER)

    tv1.heading("#0", text="INDEX", anchor=CENTER)
    tv1.heading("col0", text="PAGE ID", anchor=CENTER)
    tv1.heading("col1", text="PID", anchor=CENTER)
    tv1.heading("col2", text="LOADED", anchor=CENTER)
    tv1.heading("col3", text="L-ADDR", anchor=CENTER)
    tv1.heading("col4", text="M-ADDR", anchor=CENTER)
    tv1.heading("col5", text="D-ADDR", anchor=CENTER)
    tv1.heading("col6", text="LOADED-T", anchor=CENTER)
    tv1.heading("col7", text="-----", anchor=CENTER)
    tv1.grid(row=3, column=2, pady=5)

    h2.configure(command=tv1.yview)
    h2.grid(row=3, column=3, rowspan=1, sticky=NS)

    # Inferior
    tv1i1 = ttk.Treeview(nwMainFrame, height=1, columns=("col1"))
    tv1i1.column("#0", width=70)
    tv1i1.column("col1", width=70, anchor=CENTER)

    tv1i1.heading("#0", text="Processes", anchor=CENTER)
    tv1i1.heading("col1", text="Sim-Time", anchor=CENTER)

    tv1i1.grid(row=4, column=2, pady=5)

    tv1i2 = ttk.Treeview(nwMainFrame, height=1, columns=("col1", "col2", "col3"))
    tv1i2.column("#0", width=70)
    tv1i2.column("col1", width=70, anchor=CENTER)
    tv1i2.column("col2", width=70, anchor=CENTER)
    tv1i2.column("col3", width=70, anchor=CENTER)

    tv1i2.heading("#0", text="RAM KB", anchor=CENTER)
    tv1i2.heading("col1", text="RAM %", anchor=CENTER)
    tv1i2.heading("col2", text="V-RAM KB", anchor=CENTER)
    tv1i2.heading("col3", text="V-RAM %", anchor=CENTER)

    tv1i2.grid(row=5, column=2, pady=5)

    tv1i3 = ttk.Treeview(nwMainFrame, height=1, columns=("col1", "col2", "col3", "col4"))
    tv1i3.column("#0", width=75)
    tv1i3.column("col1", width=75, anchor=CENTER)
    tv1i3.column("col2", width=75, anchor=CENTER)
    tv1i3.column("col3", width=75, anchor=CENTER)
    tv1i3.column("col4", width=75, anchor=CENTER)

    tv1i3.heading("#0", text="P-LOADED", anchor=CENTER)
    tv1i3.heading("col1", text="P-UNLOADED", anchor=CENTER)
    tv1i3.heading("col2", text="Trashing-s", anchor=CENTER)
    tv1i3.heading("col3", text="Trashing-%", anchor=CENTER)
    tv1i3.heading("col4", text="Fragmentación", anchor=CENTER)

    tv1i3.grid(row=6, column=2, pady=5)

    #Genera una lista con los colores para los procesos, esta lista es de tamaño n segun la cantidad de procesos y posteriormente los convierte eb tags
    colors = generate_colors()
    for c in colors:
        tv.tag_configure(str(c), background=str(c))
        tv1.tag_configure(str(c), background=str(c))

    # _____________________________________________________________________
    # definicion de la funcion para actualizar el contenido de las tablas
    def updateWindowContent(algr):
        global canvas,canvas1
        #Actualizar la RAM OPT

        ramOPT = []
        for i in MMU_OPT.RAM.get_pids_loaded():
            if i == 0:
                ramOPT.append('#FFFFFF')
            else:
                ramOPT.append(colors[i])


        # Create a Figure object
        figOPT = Figure(figsize=(6, 1), dpi=100)

        # Create a table
        tableOPT = figOPT.add_subplot(111)
        tableOPT.axis('off')  # Hide the axes
        tableOPT.axis('tight')
        tableOPT.table(cellColours=[ramOPT], loc='center')
        canvas.get_tk_widget().destroy()
        # Create a Tkinter canvas that can display the figure
        canvas = FigureCanvasTkAgg(figOPT, master=nwMainFrame)
        canvas.draw()

        # Pack the canvas into the tkinter window
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=1)

        #_______________________________________________________________
        #Actualizar RAM algoritmo

        ramAlg = []
        for i in algr.RAM.get_pids_loaded():
            if i == 0:
                ramAlg.append('#FFFFFF')
            else:
                ramAlg.append(colors[i])

        # Create a Figure object
        figAlg = Figure(figsize=(6, 1), dpi=100)

        # Create a table
        tableAlg = figAlg.add_subplot(111)
        tableAlg.axis('off')  # Hide the axes
        tableAlg.axis('tight')
        tableAlg.table(cellColours=[ramAlg], loc='center')
        canvas1.get_tk_widget().destroy()
        # Create a Tkinter canvas that can display the figure
        canvas1 = FigureCanvasTkAgg(figAlg, master=nwMainFrame)
        canvas1.draw()

        # Pack the canvas into the tkinter window
        canvas1.get_tk_widget().grid(row=1, column=2, columnspan=1)

        # --------------------------------------------------------------
        # Actualizar las tabalas del OTP
        indx = 0
        indxAux = 0

        tv.delete(*tv.get_children())

        for pg in MMU_OPT.get_memory_table().values():
            aux = ""
            aux2 = ""
            ram_address = ""
            disk_address = ""

            if pg.get_flag():
                aux = "x"
                ram_address = pg.get_direction()
            else:
                disk_address = pg.get_direction()


            if pg.get_loaded_time()!=-1:
                aux2 = str(pg.get_loaded_time()) + "s"

            tv.insert(parent="", index=str(indx),tags=colors[pg.get_pid()], text=str(indx), values=(
            str(pg.get_page_id()), str(pg.get_pid()), aux, str(pg.get_ptr_id()), str(ram_address),
            str(disk_address), aux2 , "-----"))
            indx += 1
    

        tvi1.delete(*tvi1.get_children())
        tvi1.insert(parent="", index=0, text=str(MMU_OPT.get_process()), values=(str(MMU_OPT.get_simulation_time())))

        tvi2.delete(*tvi2.get_children())
        tvi2.insert(parent="", index=0, text=str(MMU_OPT.get_used_ram()), values=(
        str(MMU_OPT.get_percent_ram_used()), str(MMU_OPT.get_used_disk()), str(MMU_OPT.get_percent_disk_used())))

        tvi3.delete(*tvi3.get_children())
        tvi3.insert(parent="", index=0, text=str(MMU_OPT.get_pages_loaded()), values=(
        str(MMU_OPT.get_pages_unloaded()), str(MMU_OPT.get_thrashing()), str(MMU_OPT.get_percent_thrashing()), str(MMU_OPT.get_fragmentation())))

        # --------------------------------------------------------------
        # Actualizar las tabalas del Algoritmo comparado
        tv1.delete(*tv1.get_children())

        for pg2 in algr.get_memory_table().values():
            aux = ""
            aux2 = ""
            ram_address = ""
            disk_address = ""

            if pg2.get_flag():
                aux = "x"
                ram_address = pg2.get_direction()
            else:
                disk_address = pg2.get_direction()

            if pg2.get_loaded_time()!=-1:
                aux2 = str(pg2.get_loaded_time()) + "s"


            tv1.insert(parent="", index=str(indxAux),tags=colors[pg2.get_pid()], text=str(indxAux), values=(
            str(pg2.get_page_id()), str(pg2.get_pid()), aux, str(pg2.get_ptr_id()),
            str(ram_address), str(disk_address), aux2, "-----"))
            indxAux += 1
           

        tv1i1.delete(*tv1i1.get_children())
        tv1i1.insert(parent="", index=0, text=str(algr.get_process()), values=(str(algr.get_simulation_time())))

        tv1i2.delete(*tv1i2.get_children())
        tv1i2.insert(parent="", index=0, text=str(algr.get_used_ram()), values=(
        str(algr.get_percent_ram_used()), str(algr.get_used_disk()), str(algr.get_percent_disk_used())))

        tv1i3.delete(*tv1i3.get_children())
        tv1i3.insert(parent="", index=0, text=str(algr.get_pages_loaded()), values=(
        str(algr.get_pages_unloaded()), str(algr.get_thrashing()), str(algr.get_percent_thrashing()), str(algr.get_fragmentation())))

    # print(MMU_OPT.RAM.get_pids_loaded())
    # print(MMU_OPT.get_memory_table()[1])
    # ___________________________________________________________________________
    # Funcion que inicia el programa
    def startProgram():

        global selected, instructions, MMU_OPT, MMU_RND, MMU_MRU, MMU_FIFO, MMU_SC, fileSelected, filename
        print(fileSelected)
        print(filename)
        if fileSelected == True:
            instructions = open_document(filename)
        else:
            # fileGenerator(0,10,176)
            fileGenerator(seedEntry.get(), int(pselected.get()), int(opselected.get()))
            instructions = open_document("generatedFile.txt")

        # _____________________________________________________________________
        # For de la ejecución de los algoritmos y actualización de las tablas
        from OPT import OPT
        OPT = OPT(instructions, TOTAL_RAM, PAGE_SIZE)
        order_to_unload = OPT.process_commands()
        RAM1 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
        RAM2 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
        DISK1 = Disk(PAGE_SIZE)
        DISK2 = Disk(PAGE_SIZE)
        MMU_OPT = MMU_OPT(RAM1, DISK1, order_to_unload)

        global paused

        if selected.get() == "RND":

            MMU_RND = MMU_RND(RAM2, DISK2, seedEntry.get())
            for instruction in instructions:
                while paused:
                    print("detenido")
                    time.sleep(1)

                MMU_OPT.simulate(instruction)

                MMU_RND.simulate(instruction)

                updateWindowContent(MMU_RND)
                time.sleep(0.005)
        if selected.get() == "FIFO":

            MMU_FIFO = MMU_FIFO(RAM2, DISK2)

            for instruction in instructions:
                while paused:
                    print("detenido")
                    time.sleep(1)

                MMU_OPT.simulate(instruction)

                MMU_FIFO.simulate(instruction)

                updateWindowContent(MMU_FIFO)

        if selected.get() == "MRU":

            MMU_MRU = MMU_MRU(RAM2, DISK2)

            for instruction in instructions:
                while paused:
                    print("detenido")
                    time.sleep(1)

                MMU_OPT.simulate(instruction)

                MMU_MRU.simulate(instruction)

                updateWindowContent(MMU_MRU)

        if selected.get() == "SC":

            MMU_SC = MMU_SC(RAM2, DISK2)

            for instruction in instructions:
                while paused:
                    print("detenido")
                    time.sleep(1)

                MMU_OPT.simulate(instruction)

                MMU_SC.simulate(instruction)

                updateWindowContent(MMU_SC)

    def stoploop():
        print("Llego aqui")
        global paused
        if paused:
            paused = False
        else:
            paused = True
        print(paused)

    btnStop = Button(nwMainFrame, text="Pausar/Correr", command=stoploop)
    btnStop.grid(row=7, column=0)
    btnStop.config(cursor="hand2")


    startProgram()


# Esta funcion crea un thread para manejar la ventana mientras el proceso del algoritmo y la actualizacion corren detras

def createAndStartThread():
    subproceso = subproceso = threading.Thread(target=openNewWindow)
    subproceso.start()


# Creacion del frame raiz
root = Tk()

root.title("Simulador SO")

root.resizable(True, True)

root.config(bd=10)

root.config(relief="groove")

# Creacion del frame principal
mainFrame = Frame(root)

mainFrame.pack(fill="both")

mainFrame.config(width="720", height="650")

# Creacion del titulo del frame
Label(mainFrame, text="Simulador de Algoritmos de paginación", justify="center").grid(row=0, column=1, pady=4)

# Label y contenedor de la entrada de la semilla
seedLabel = Label(mainFrame, text="Semilla")
seedLabel.grid(row=1, column=0, padx=4, pady=4)

seedEntry = Entry(mainFrame)
seedEntry.grid(row=1, column=1, padx=4, pady=4)
seedEntry.config(justify="center")

# Creacion del combobox Algoritmo
algotLabel = Label(mainFrame, text="Algoritmo")
algotLabel.grid(row=2, column=0, padx=4, pady=4)

choices = ["FIFO", "SC", "MRU", "RND"]
selected = StringVar(mainFrame)
selected.set(choices[0])

opmAlgo = OptionMenu(mainFrame, selected, *choices)
opmAlgo.grid(row=2, column=1, padx=4, pady=4)
opmAlgo.config(cursor="hand2")

# Creacion del combobox N procesos
pLabel = Label(mainFrame, text="Numero de procesos")
pLabel.grid(row=3, column=0, pady=4)

pchoices = ["10", "50", "100"]
pselected = StringVar(mainFrame)
pselected.set(pchoices[0])

opmp = OptionMenu(mainFrame, pselected, *pchoices)
opmp.grid(row=3, column=1, pady=4)
opmp.config(cursor="hand2")

# Creacion del combobox N operaciones
opLabel = Label(mainFrame, text="Numero de operaciones")
opLabel.grid(row=3, column=2, pady=4)

opchoices = ["500", "1000", "5000"]
opselected = StringVar(mainFrame)
opselected.set(opchoices[0])

opmAlgo = OptionMenu(mainFrame, opselected, *opchoices)
opmAlgo.grid(row=3, column=3, pady=4)
opmAlgo.config(cursor="hand2")

# Input del archivo a cargar
button_explore = Button(mainFrame, text="Archivo", command=browseFiles)
button_explore.grid(column=0, row=4, padx=4, pady=4)
button_explore.config(cursor="hand2")

label_file_explorer = Label(mainFrame, text="File Explorer", width=65, height=4, fg="blue")
label_file_explorer.grid(column=1, row=4, padx=4)

# Cracion del boton de ejecucion

"""
## VERIFICAR

filename_test = "generatedFile.txt"  # CAMBIAR
seed = 1  # CAMBIAR

instructions = open_document(filename_test)
OPT = OPT(instructions, TOTAL_RAM, PAGE_SIZE)
order_to_unload = OPT.process_commands()
RAM1 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
RAM2 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
DISK1 = Disk(PAGE_SIZE)
DISK2 = Disk(PAGE_SIZE)
MMU_OPT = MMU_OPT(RAM1, DISK1, order_to_unload)

#  SE DEBE VALIDAR SEGUN ALGORITMO SELECCIONADO
MMU_RND = MMU_RND(RAM2, DISK2, seed)
"""

btnRun = Button(mainFrame, text="Correr", command=createAndStartThread)
btnRun.grid(row=5, column=1)
btnRun.config(cursor="hand2")

root.mainloop()
