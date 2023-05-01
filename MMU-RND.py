import math
import random
from MMU import MMU
from RAM import RAM
from Disk import Disk


class MMU_RND(MMU):
    def __init__(self, instructions, ram, disk, seed):
        super().__init__(instructions, ram, disk)
        self.seed = seed

    def unload_page(self):
        random.seed(self.seed)
        index = random.randint(0, self.RAM.amount_pages)
        page_to_unload = self.RAM.memory[index]

        real_page = self.RAM.unload_page(page_to_unload.get_page_id())
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

            if self.RAM.available_ram >= page_size:
                self.increment_simulation_time()  # HIT
                page_load = self.RAM.load_page(pages[i])
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria
            else:
                self.unload_page()
                self.increment_sim_thras_time()  # FAILURE
                page_load = self.RAM.load_page(pages[i])
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria

        self.increment_ptr_id()

    def use(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for page_id in pages_in_ptr:
            if not page_id in pages_loaded:
                if self.RAM.available_ram >= self.RAM.page_size:
                    self.increment_simulation_time()  # HIT
                    page_to_load = self.disk.unload_page(self.memory_table[page_id])
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])
                else:
                    self.unload_page()
                    self.increment_sim_thras_time()  # FAILURE
                    page_to_load = self.memory_table[page_id]
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])

    def delete(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for p in pages_in_ptr:
            if p in pages_loaded:
                page_unloaded = self.RAM.unload_page(p)
                size = page_unloaded.get_size()
                if size < self.RAM.page_size:
                    self.decrement_fragmentation(self.RAM.page_size-size)
            else:
                page_to_unload = self.memory_table[p]
                page_unloaded = self.disk.unload_page(page_to_unload)
                size = page_unloaded.get_size()
                if size < self.RAM.page_size:
                    self.decrement_fragmentation(self.RAM.page_size - size)
        self.delete_from_memory_table(p)

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

        print("RAM\n")
        print(self.RAM.available_ram)
        [print(p) for p in self.RAM.memory]
        print("DISK\n")
        [print(p) for p in self.disk.memory]
        print("MEM TABLE\n")
        [print(p, " - ", self.memory_table[p]) for p in self.memory_table]
        print("FRAGMENTATION")
        print(self.fragmentation)
        print("SIMULATION TIME")
        print(self.simulation_time)
        print("THRASHING")
        print(self.thrashing)


instructions1 = [['new', '1', '380'], ['new', '2', '400'], ['new', '1', '400'], ['new', '2', '100'], ['use', '1'],
                 ['use', '2'], ['new', '3', '450'], ['delete', '3'], ['kill', '1']]
order_to_unload1 = [(2, 5), (2, 6), [(3, 9), (3, 10), (3, 11), (3, 12)], [(1, 1), (1, 2), (1, 3), (1, 4)]]
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
ram1 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
disk1 = Disk(PAGE_SIZE)
SEED = 1
x = MMU_RND(instructions1, ram1, disk1, SEED)
print(x.simulate())
