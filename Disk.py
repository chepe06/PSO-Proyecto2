class Disk:

    def __init__(self, page_size):
        self.used_memory = 0
        self.page_size = page_size
        self.memory = []

    def get_address(self, page):
        return self.memory.index(page)

    def increase_disk_use(self):
        self.used_memory = self.used_memory + self.page_size

    def decrease_disk_use(self):
        self.used_memory = self.used_memory - self.page_size

    def load_page(self, page):
        self.increase_disk_use()
        temp = self.memory
        index = len(temp)
        page.set_direction(index)  # Se guarda la dirección en Disco
        temp.append(page)
        self.memory = temp

    def unload_page(self, page):
        self.decrease_disk_use()
        temp = self.memory
        temp.remove(page)
        self.memory = temp
        return page
