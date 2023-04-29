class RAM:

    def __init__(self, ram=400, amount_pages=100, page_size=4):  # CAMBIAR
        self.total_ram = ram
        self.available_ram = ram
        self.amount_pages = amount_pages
        self.page_size = page_size  # ram // amount_pages
        self.memory = self.create_empty_ram()

    # GETTERS
    def get_memory(self):
        return self.memory

    # FUNCTIONS

    def create_empty_ram(self):
        temp = []
        for i in range(self.amount_pages):
            temp.append(0)
        return temp

    def is_full(self):
        return self.available_ram == 0

    def increase_ram(self):
        self.available_ram = self.available_ram + self.page_size

    def decrease_ram(self):
        self.available_ram = self.available_ram - self.page_size

    def load_page(self, page):
        self.decrease_ram()
        temp = self.get_memory()
        index = temp.index(0)
        page[1].set_direction(index)  # Se agrega la ubicación dentro de la RAM
        temp[index] = page
        self.memory = temp

    def unload_page(self, page):  # Page (ptr, page_id) mientras que en RAM (pid, Clase página)
        self.increase_ram()
        temp = self.memory
        page_unloaded = [p for p in self.memory if page[1] == p[1].get_page_id()][0]
        print(page_unloaded)
        index = temp.index(page_unloaded)
        temp[index] = 0
        self.memory = temp
        return page_unloaded
