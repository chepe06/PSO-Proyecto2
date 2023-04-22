class MMU:
    def __init__(self):
        self.real_memory = 400
        self.real_memory_used = 0
        self.RAM = []  # VECTOR CON 0`s de tamaño 100(Páginas), se utiliza para graficar

        self.virtual_memory_used = 0
        self.fragmentation = 0

        self.ptr_id = 0

        # MAPA DE MEMORIA
        self.table = {}
        self.pages_loaded = 0
        self.pages_unloaded = 0

        self.simulation_time = 0
        self.thrashing = 0

    def get_table(self):
        return self.table

    def update_table(self, key, value):  # KEY -> Puntero Lógico // VALUE -> (PID, [ PAGE ID, ])
        temp = self.table
        temp[key] = value
        self.table = temp

    def new(self, pid, size):
        pass

    def use(self, ptr):
        pass

    def delete(self, ptr):
        pass

    def kill(self, pid):
        pass
