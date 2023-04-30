import math
from MMU import MMU
from RAM import RAM
from Disk import Disk


class MMU_OPT(MMU):
    def __init__(self, instructions, ram, disk, order_to_unload):
        super().__init__(instructions, ram, disk)
        self.order_to_unload = order_to_unload

    def unload_page(self):
        page_to_unload = self.order_to_unload.pop(0)  # Página o Páginas por unload
        if isinstance(page_to_unload, list):
            for p in page_to_unload:
                self.decrement_pages_loaded()
                self.increment_pages_unloaded()
                page_id = p[1]
                real_page = self.RAM.unload_page(page_id)
                real_page.set_flag(False)
                self.add_page_to_memory_table(real_page.page_id,
                                              real_page)  # Se actualiza de la tabla de memoria
                self.disk.load_page(real_page)
        else:
            self.decrement_pages_loaded()
            self.increment_pages_unloaded()
            real_page = self.RAM.unload_page(page_to_unload)
            real_page.set_flag(False)
            self.add_page_to_memory_table(real_page.page_id,
                                          real_page)  # Se actualiza de la tabla de memoria
            self.disk.load_page(real_page)

    def new(self, pid, size):
        page_size = self.RAM.page_size
        pages = []

        if size > page_size:  # En caso de que se necesite más de una página
            pages_amount = math.ceil(size / page_size)
            fragmentation = (pages_amount * page_size) - size
            for i in range(pages_amount):
                if size < page_size:
                    page = self.create_page(pid, size)
                else:
                    page = self.create_page(pid, page_size)
                size = size - page_size
                pages.append(page)
                self.relate_ptr_to_pages(page.page_id)  # Se relaciona el ptr con el page_id
                self.increment_page_id()

            self.increment_fragmentation(fragmentation)

        else:
            page = self.create_page(pid, page_size)
            pages.append(page)
            self.relate_ptr_to_pages(page.page_id)  # Se relaciona el ptr con el page_id
            self.increment_page_id()
            fragmentation = page_size - size
            self.increment_fragmentation(fragmentation)

        self.relate_pid_to_ptrs(pid)  # Se relaciona el pid con el ptr

        for i in range(len(pages)):
            self.increment_pages_loaded()  # Se aumenta las páginas cargadas

            if self.RAM.available_ram >= page_size:
                page_load = self.RAM.load_page(pages[i])
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria
            else:
                self.unload_page()
                page_load = self.RAM.load_page(pages[i])
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria

        self.increment_ptr_id()

    def use(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM if page.ptr_id == ptr_id]

        for page_id in pages_in_ptr:
            if not page_id in pages_loaded:
                if self.RAM.available_ram >= self.RAM.page_size:
                    self.RAM.decrease_ram()
                    page_to_load = self.disk.unload_page(self.memory_table[page_id])
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])
                else:
                    self.unload_page()
                    page_to_load = self.memory_table[page_id]
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])

    def delete(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM if page.ptr_id == ptr_id]

        for p in pages_in_ptr:
            if p in pages_loaded:
                self.RAM.unload_page(p)
                self.delete_from_memory_table(p)
            else:
                page_to_unload = self.memory_table[p]
                self.disk.unload_page(page_to_unload)

        self.ptrs.pop(ptr_id)

    def kill(self, pid):
        ptrs = self.pids[pid]
        for ptr_id in ptrs:
            if ptr_id in self.ptrs:
                self.delete(ptr_id)
        self.pids.pop(pid)

    def simulate(self):
        for instruction in self.instructions:
            if instruction[0] == "new":
                pid = int(instruction[1])
                size = int(instruction[2])
                self.new(pid, size)

            elif instruction[0] == "use":
                ptr_id = int(instruction[1])
                self.use(ptr_id)

            elif instruction[0] == "delete":
                ptr_id = int(instruction[1])
                self.delete(ptr_id)

            elif instruction[0] == "kill":
                pid = int(instruction[1])
                self.delete(pid)


            """
            print("RAM\n")
            [print(p) for p in self.RAM.memory]
            print("DISK")
            [print(p) for p in self.disk.memory]
            print("")
            """
        # [print(p, " - ", self.memory_table[p]) for p in self.memory_table]


instructions1 = [['new', '1', '400'], ['new', '2', '400'], ['new', '3', '400'], ['new', '4', '100'],
                 ['new', '5', '500']]
order_to_unload1 = [[(1, 1), (1, 2), (1, 3), (1, 4)], [(2, 5), (2, 6), (2, 7), (2, 8)]]
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
ram1 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
disk1 = Disk(PAGE_SIZE)
x = MMU_OPT(instructions1, ram1, disk1, order_to_unload1)
print(x.simulate())
