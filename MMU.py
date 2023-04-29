from Page import Page


class MMU:
    def __init__(self, instructions, ram, disk):
        self.instructions = instructions
        self.RAM = ram
        self.disk = disk
        self.fragmentation = 0
        self.ptr_id = 1
        self.page_id = 1

        # MAPA DE MEMORIA
        self.table = {}
        self.pages_loaded = 0
        self.pages_unloaded = 0

        self.simulation_time = 0
        self.thrashing = 0

    def increment_page_id(self):
        self.page_id = self.page_id + 1

    def increment_ptr_id(self):
        self.ptr_id = self.ptr_id + 1

    def increment_fragmentation(self, size):
        self.fragmentation = self.fragmentation + size

    def decrement_fragmentation(self, size):
        self.fragmentation = self.fragmentation - size

    def increment_pages_loaded(self):
        self.pages_loaded = self.pages_loaded + 1

    def decrement_pages_loaded(self):
        self.pages_loaded = self.pages_loaded - 1

    def increment_pages_unloaded(self):
        self.pages_unloaded = self.pages_unloaded + 1

    def decrement_pages_unloaded(self):
        self.pages_unloaded = self.pages_unloaded - 1

    def create_page(self, size):
        return Page(self.page_id, -1, True, size)

    def get_table(self):
        return self.table

    def update_table(self, key, value):  # KEY -> PID - VALUE -> {} // KEY -> PTR - VALUE -> [ PAGE ID, ]
        #
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
