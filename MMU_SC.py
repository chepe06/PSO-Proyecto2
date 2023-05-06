import math
from MMU import MMU
from Page_SC import Page_SC

#from RAM import RAM
#from Disk import Disk


class MMU_SC(MMU):
    def __init__(self, ram, disk):
        super().__init__(ram, disk)
        self.second_chance_list = []

    def create_pages(self, pid, size, page_size):
        pages = []
        if size > page_size:  # En caso de que se necesite más de una página
            pages_amount = math.ceil(size / page_size)
            fragmentation = (pages_amount * page_size) - size
            for i in range(pages_amount):
                if size < page_size:
                    page = self.create_page(pid, size, self.simulation_time)
                else:
                    page = self.create_page(pid, page_size, self.simulation_time)
                size = size - page_size
                pages.append(page)
                self.relate_ptr_to_pages(page.page_id)  # Se relaciona el ptr con el page_id
                self.increment_page_id()

            self.increment_fragmentation(fragmentation)

        else:
            page = self.create_page(pid, page_size, self.simulation_time)
            pages.append(page)
            self.relate_ptr_to_pages(page.page_id)  # Se relaciona el ptr con el page_id
            self.increment_page_id()
            fragmentation = page_size - size
            self.increment_fragmentation(fragmentation)

        self.relate_pid_to_ptrs(pid)  # Se relaciona el pid con el ptr

        return pages

    def create_page(self, pid, size, loaded_time):
        return Page_SC(pid, self.ptr_id, self.page_id, -1, True, size, loaded_time)

    def unload_page(self, ptr_id):
        sc = True
        while sc:
            for page in self.second_chance_list:
                if page.get_life() == 0 and page.get_ptr_id() != ptr_id:
                    self.second_chance_list.remove(page)
                    real_page = self.RAM.unload_page(page.get_page_id())
                    real_page.set_flag(False)
                    real_page.set_loaded_time(-1)
                    size = real_page.get_size()
                    if size < self.RAM.page_size:
                        self.decrement_fragmentation(self.RAM.page_size - size)
                    self.add_page_to_memory_table(real_page.page_id,
                                                  real_page)  # Se actualiza de la tabla de memoria
                    self.disk.load_page(real_page)
                    sc = False
                    break
                else:
                    page.set_life(0)

    def new(self, pid, size):
        page_size = self.RAM.page_size
        pages = self.create_pages(pid, size, page_size)

        second_chance_list = []
        for i in range(len(pages)):

            if self.RAM.available_ram >= page_size:
                self.increment_simulation_time()  # HIT
                page_load = self.RAM.load_page(pages[i])
                second_chance_list.append(page_load)  # SE AGREGA A LA COLA
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria
            else:
                self.unload_page(self.ptr_id)
                self.increment_sim_thras_time()  # FAILURE
                page_load = self.RAM.load_page(pages[i])
                second_chance_list.append(page_load)  # SE AGREGA A LISTA TEMPORAL
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria

        [self.second_chance_list.append(p) for p in second_chance_list]  # SE AGREGA A LA COLA PRINCIPAL
        self.increment_ptr_id()

    def use(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for page_id in pages_in_ptr:
            if not page_id in pages_loaded:  # FAILURE
                self.increment_sim_thras_time()
                if self.RAM.available_ram < self.RAM.page_size:
                    self.unload_page(ptr_id)

                page_to_load = self.disk.unload_page(self.memory_table[page_id])
                page_to_load.set_flag(True)
                page_to_load.set_loaded_time(self.simulation_time)
                page_to_load.set_life(1)
                page_load = self.RAM.load_page(self.memory_table[page_id])
                self.second_chance_list.append(page_load)  # SE AGREGA A LA COLA
                self.add_page_to_memory_table(page_load.page_id,
                                              page_load)  # SE ACTUALIZA DE LA TABLA DE MEMORIA

            else:  # HIT
                for p in self.second_chance_list:
                    if p.get_page_id() == page_id:
                        p.set_life(1)

                self.increment_simulation_time()

    def delete(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for p in pages_in_ptr:
            if p in pages_loaded:
                page_unloaded = self.RAM.unload_page(p)
                size = page_unloaded.get_size()
                if size < self.RAM.page_size:
                    self.decrement_fragmentation(self.RAM.page_size - size)
                # SE ELIMINA DE LA COLA
                self.second_chance_list.remove(page_unloaded)
            else:
                page_to_unload = self.memory_table[p]
                self.disk.unload_page(page_to_unload)
            self.delete_from_memory_table(p)

        self.ptrs.pop(ptr_id)

    def kill(self, pid):
        ptrs = self.pids[pid]
        for ptr_id in ptrs:
            if ptr_id in self.ptrs:
                self.delete(ptr_id)
        self.pids.pop(pid)

"""
# COMPUTER
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
RAM = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
DISK = Disk(PAGE_SIZE)
MMU_SC = MMU_SC(RAM, DISK)

# INSTRUCTIONS = [['new', '6', '842'], ['use', '1'], ['use', '1'], ['use', '1'], ['new', '3', '572'], ['new', '1', '301'], ['use', '2'], ['new', '3', '948'], ['delete', '4'], ['new', '10', '895'], ['use', '1'], ['use', '3'], ['kill', '1'], ['use', '1'], ['new', '5', '750'], ['kill', '10'], ['use', '1'], ['use', '1'], ['use', '6'], ['use', '1'], ['use', '6'], ['new', '8', '667'], ['use', '6'], ['use', '7'], ['use', '7'], ['use', '7'], ['kill', '6'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '6'], ['kill', '5'], ['new', '7', '840'], ['use', '7'], ['new', '4', '742'], ['use', '7'], ['use', '8'], ['use', '7'], ['use', '9'], ['new', '7', '254'], ['use', '9'], ['use', '9'], ['delete', '10'], ['use', '9'], ['new', '4', '704'], ['use', '7'], ['use', '11'], ['use', '7'], ['use', '11'], ['use', '11'], ['use', '7'], ['use', '7'], ['new', '8', '63'], ['use', '11'], ['use', '12'], ['use', '12'], ['use', '11'], ['use', '11'], ['new', '3', '899'], ['use', '11'], ['delete', '13'], ['new', '9', '503'], ['use', '14'], ['kill', '9'], ['new', '2', '313'], ['use', '12'], ['new', '2', '452'], ['use', '16'], ['use', '12'], ['use', '12'], ['new', '4', '110'], ['use', '12'], ['delete', '16'], ['use', '12'], ['use', '17'], ['use', '12'], ['use', '12'], ['use', '12'], ['use', '17'], ['use', '12'], ['use', '17'], ['use', '17'], ['new', '2', '733'], ['use', '17'], ['new', '8', '158'], ['use', '19'], ['kill', '8'], ['use', '18'], ['new', '7', '819'], ['use', '17'], ['use', '20'], ['use', '18'], ['use', '17'], ['use', '20'], ['use', '20'], ['use', '17'], ['use', '17'], ['use', '20'], ['use', '18'], ['new', '4', '412'], ['use', '18'], ['delete', '20'], ['use', '21'], ['use', '18'], ['use', '18'], ['new', '4', '71'], ['new', '2', '567'], ['use', '22'], ['new', '7', '893'], ['new', '7', '224'], ['use', '25'], ['use', '22'], ['use', '23'], ['kill', '2'], ['use', '25'], ['use', '22'], ['use', '25'], ['use', '25'], ['new', '3', '97'], ['use', '25'], ['use', '22'], ['use', '22'], ['use', '22'], ['use', '25'], ['use', '22'], ['use', '22'], ['use', '22'], ['kill', '7'], ['use', '26'], ['use', '26'], ['new', '4', '833'], ['use', '27'], ['use', '27'], ['delete', '26'], ['use', '27'], ['new', '4', '583'], ['use', '28'], ['new', '4', '613'], ['use', '29'], ['delete', '29'], ['new', '3', '437'], ['use', '30'], ['use', '30'], ['use', '30'], ['kill', '3'], ['new', '4', '178'], ['use', '31'], ['new', '4', '933'], ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['delete', '32'], ['new', '4', '328'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['kill', '4']]
INSTRUCTIONS = [['new', '1', '400'], ['new', '2', '400'], ['new', '3', '400'], ['use', '1'], ['new', '4', '600']]
for x in INSTRUCTIONS:
    # print("RECENTLY USED")
    # [print(p) for p in MMU_MRU.recently_used]
    MMU_SC.simulate(x)
"""
