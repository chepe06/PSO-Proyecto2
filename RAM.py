class RAM:

    def __init__(self):
        self.setFreeRam(400)
        self.setMemory(self.createEmptyRam())
    
    # seccion de los gets
    
    def getFreeRam(self):
        return self.__maxSize

    def getMemory(self):
        return self.__memory


    # seccion de los sets
    def setFreeRam(self, maxSize):
        self.__maxSize = maxSize

    def setMemory(self, memory):
        self.__memory = memory


    #funciones


#se crea una ram vacia de tamaño 100
    def createEmptyRam(self):
        tempList = []
        for i in range(100):
            tempList.append(0)
        return tempList


#se requiere saber si la RAM esta llena sabiendo el campo disponible de la RAM si es 0 o menor 
    def isFull(self):
        return self.getFreeRam() <= 0


# se requiere asignar una pagina
    def allocatePage(self, page):
        tempFreeRam = self.getFreeRam()#se pregunta cuanto hay disponible
        tempFreeRam -= 4 #seresta 4
        self.setFreeRam(tempFreeRam)#se actualiza la memoria disponible
        tempMem = self.getMemory()
        index = tempMem.index(0)
        tempMem.remove(0)
        tempMem.insert(index, page)
        self.setMemory(tempMem)

 #se requiere borrar una pagina    
    def removePage(self, page):
        tempFreeRam = self.getFreeRam()#se pregunta cuanto hay disponible
        tempMem = self.getMemory()
        tempFreeRam += 4 # se le suman 4
        index = tempMem.index(page)#se capta la pagina
        tempMem.remove(page)#se borra
        tempMem.insert(index, 0)
        self.setFreeRam(tempFreeRam)
        self.setMemory(tempMem)
