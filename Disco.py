class Disco:

    def __init__(self):
        self.setUsedMemory(0)
        self.setMemory([])
    
    #seccion de gets
    #devuelve la meroria total
    def getMemory(self):
        return self.__memory
#devuelve pero la memoria usada hasta el momento
    def getUsedMemory(self):
        return self.__usedMemory


    # seccion de set
    #se setea la memoria total
    def setMemory(self, memory):
        self.__memory = memory
    #se setea la memoria usada
    def setUsedMemory(self, usedMemory):
        self.__usedMemory = usedMemory


    # funciones

    
    def getAddr(self, page):
        return self.getMemory().index(page)

    def allocatePage(self, page):
        tempMem = self.getMemory()
        tempMem.append(page)
        tempUsedMemory = self.getUsedMemory()
        tempUsedMemory += 4 #es 4 segun el proyecto especificacion 
        self.setUsedMemory(tempUsedMemory)
        self.setMemory(tempMem)
    
    def removePage(self, page):
        tempMem = self.getMemory()
        tempUsedMemory = self.getUsedMemory()
        tempUsedMemory -= 4
        index = tempMem.index(page)
        tempMem.remove(page)
        tempMem.insert(index, 0)
        self.setUsedMemory(tempUsedMemory)
        self.setMemory(tempMem)