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
                page_id = p[1]
                real_page = self.RAM.unload_page(page_id)
                real_page.set_flag(False)
                self.add_page_to_memory_table(real_page.page_id,
                                              real_page)  # Se actualiza de la tabla de memoria
                self.disk.load_page(real_page)
        else:
            real_page = self.RAM.unload_page(page_to_unload[1])
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
                self.increment_simulation_time()  # FAILURE
                if self.RAM.available_ram >= self.RAM.page_size:
                    page_to_load = self.disk.unload_page(self.memory_table[page_id])
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])
                else:
                    self.unload_page()
                    page_to_load = self.disk.unload_page(self.memory_table[page_id])
                    page_to_load.set_flag(True)
                    self.add_page_to_memory_table(page_to_load.page_id,
                                                  page_to_load)  # Se actualiza de la tabla de memoria
                    self.RAM.load_page(self.memory_table[page_id])
            else:
                self.increment_simulation_time()  # HIT

    def delete(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for p in pages_in_ptr:
            if p in pages_loaded:
                page_unloaded = self.RAM.unload_page(p)
                size = page_unloaded.get_size()
                if size < self.RAM.page_size:
                    self.decrement_fragmentation(self.RAM.page_size - size)
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
            self.increment_simulation_time()
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
                self.kill(pid)

        print("RAM\n")
        print(self.RAM.available_ram)
        [print(p) for p in self.RAM.memory]
        print("DISK\n")
        print(self.disk.used_memory)
        [print(p) for p in self.disk.memory]
        print("MEM TABLE\n")
        [print(p, " - ", self.memory_table[p]) for p in self.memory_table]
        print("FRAGMENTATION")
        print(self.fragmentation)
        print("SIMULATION TIME")
        print(self.simulation_time)
        print("THRASHING")
        print(self.thrashing)


instructions1 = [['new', '6', '842'], ['use', '1'], ['use', '1'], ['use', '1'], ['new', '3', '572'],
                 ['new', '1', '301'], ['use', '2'], ['new', '3', '948'], ['delete', '4'], ['new', '10', '895'],
                 ['use', '1'], ['use', '3'], ['kill', '1'], ['use', '1'], ['new', '5', '750'], ['kill', '10'],
                 ['use', '1'], ['use', '1'], ['use', '6'], ['use', '1'], ['use', '6'], ['new', '8', '667'],
                 ['use', '6'], ['use', '7'], ['use', '7'], ['use', '7'], ['kill', '6'], ['use', '7'], ['use', '7'],
                 ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '6'], ['kill', '5'],
                 ['new', '7', '840'], ['use', '7'], ['new', '4', '742'], ['use', '7'], ['use', '8'], ['use', '7'],
                 ['use', '9'], ['new', '7', '254'], ['use', '9'], ['use', '9'], ['delete', '10'], ['use', '9'],
                 ['new', '4', '704'], ['use', '7'], ['use', '11'], ['use', '7'], ['use', '11'], ['use', '11'],
                 ['use', '7'], ['use', '7'], ['new', '8', '63'], ['use', '11'], ['use', '12'], ['use', '12'],
                 ['use', '11'], ['use', '11'], ['new', '3', '899'], ['use', '11'], ['delete', '13'],
                 ['new', '9', '503'], ['use', '14'], ['kill', '9'], ['new', '2', '313'], ['use', '12'],
                 ['new', '2', '452'], ['use', '16'], ['use', '12'], ['use', '12'], ['new', '4', '110'], ['use', '12'],
                 ['delete', '16'], ['use', '12'], ['use', '17'], ['use', '12'], ['use', '12'], ['use', '12'],
                 ['use', '17'], ['use', '12'], ['use', '17'], ['use', '17'], ['new', '2', '733'], ['use', '17'],
                 ['new', '8', '158'], ['use', '19'], ['kill', '8'], ['use', '18'], ['new', '7', '819'], ['use', '17'],
                 ['use', '20'], ['use', '18'], ['use', '17'], ['use', '20'], ['use', '20'], ['use', '17'],
                 ['use', '17'], ['use', '20'], ['use', '18'], ['new', '4', '412'], ['use', '18'], ['delete', '20'],
                 ['use', '21'], ['use', '18'], ['use', '18'], ['new', '4', '71'], ['new', '2', '567'], ['use', '22'],
                 ['new', '7', '893'], ['new', '7', '224'], ['use', '25'], ['use', '22'], ['use', '23'], ['kill', '2'],
                 ['use', '25'], ['use', '22'], ['use', '25'], ['use', '25'], ['new', '3', '97'], ['use', '25'],
                 ['use', '22'], ['use', '22'], ['use', '22'], ['use', '25'], ['use', '22'], ['use', '22'],
                 ['use', '22'], ['kill', '7'], ['use', '26'], ['use', '26'], ['new', '4', '833'], ['use', '27'],
                 ['use', '27'], ['delete', '26'], ['use', '27'], ['new', '4', '583'], ['use', '28'],
                 ['new', '4', '613'], ['use', '29'], ['delete', '29'], ['new', '3', '437'], ['use', '30'],
                 ['use', '30'], ['use', '30'], ['kill', '3'], ['new', '4', '178'], ['use', '31'], ['new', '4', '933'],
                 ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['delete', '32'],
                 ['new', '4', '328'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'],
                 ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'],
                 ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['kill', '4']]
order_to_unload1 = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 10), (2, 11), (2, 12), (2, 13), (3, 16), (3, 17),
                    (3, 18), (3, 19), [(2, 14), (2, 15), (2, 10), (2, 11), (2, 12), (2, 13)], (1, 6), (1, 7), (1, 8),
                    (1, 9), [(5, 30), (5, 31), (5, 32), (5, 33), (5, 34), (5, 35), (5, 36), (5, 37), (5, 38)], (1, 1),
                    (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 1), (6, 39), (6, 40), (6, 41),
                    (6, 42), (6, 43), (6, 44), (6, 45), (1, 2), (1, 3), (1, 1), (1, 4), (1, 5), (1, 6), (1, 7), (6, 46),
                    (6, 39), (6, 40), (6, 41), (6, 42), (6, 43), (6, 44),
                    [(1, 8), (1, 9), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)], (6, 45), (6, 39), (6, 40),
                    (6, 41), (6, 42), (7, 47), (7, 48), (7, 49), (7, 50), (7, 51), (6, 43), (6, 44), (6, 46), (6, 39),
                    (6, 40), (7, 52), (7, 53), (7, 47), (7, 48), (7, 49), (7, 50), (8, 54), (8, 55), (8, 56), (8, 57),
                    (8, 58), (8, 59), (8, 60), (8, 61), (8, 62), (7, 51), (7, 47), (7, 48), (7, 49), (7, 50), (9, 63),
                    (9, 64), (9, 65), (9, 66), (9, 67), (9, 68), (9, 69), (9, 70), (7, 52), (7, 53), (7, 47), (7, 48),
                    (7, 49), (7, 50), [(8, 54), (8, 55), (8, 56), (8, 57), (8, 58), (8, 59), (8, 60), (8, 61), (8, 62)],
                    (7, 51), (7, 47), (7, 48), (7, 49), (7, 50), (9, 63), (9, 64), (9, 65),
                    [(10, 71), (10, 72), (10, 73)],
                    [(9, 66), (9, 67), (9, 68), (9, 69), (9, 70), (9, 63), (9, 64), (9, 65)], (11, 74), (11, 75),
                    (11, 76), (11, 77), (11, 78), (7, 52), (7, 53), (7, 47), (7, 48), (7, 49), (11, 79), (11, 80),
                    (11, 81), (11, 74), (11, 75), (7, 50), (7, 51), (7, 47), (7, 48), (7, 49), (11, 76), (11, 77),
                    (11, 78), (11, 74), (11, 75), [(7, 52), (7, 53), (7, 47), (7, 48), (7, 49), (7, 50), (7, 51)],
                    (12, 82), (11, 79), (11, 80), (11, 81), (11, 74), (11, 75), (11, 76), (11, 77),
                    [(13, 83), (13, 84), (13, 85), (13, 86), (13, 87), (13, 88), (13, 89), (13, 90), (13, 91)],
                    [(11, 78), (11, 74), (11, 75), (11, 76), (11, 77), (11, 79), (11, 80), (11, 81)],
                    [(15, 98), (15, 99), (15, 100), (15, 101)], [(12, 82)], (18, 109), (18, 110), (18, 111), (18, 112),
                    (18, 113), (18, 114), (18, 115), (18, 116), (18, 109), (18, 110), (17, 107), (20, 119), (17, 108),
                    (17, 107), (20, 120), (20, 121), (20, 122), (20, 123), (20, 124), (20, 125), (20, 126), (20, 127),
                    (20, 119), (17, 107), (17, 108), (18, 109), (18, 110), (18, 111), (18, 112), (18, 113), (18, 114),
                    (18, 115), (20, 119), (20, 120), [(17, 107), (17, 108)],
                    [(20, 121), (20, 122), (20, 123), (20, 124), (20, 125), (20, 126), (20, 127), (20, 119), (20, 120)],
                    (18, 116), (18, 109), (18, 110), (21, 128), (21, 129), (21, 130), (18, 111), (18, 112), (18, 113),
                    [(21, 131), (21, 132), (21, 128), (21, 129), (21, 130)],
                    [(18, 114), (18, 115), (18, 109), (18, 110), (18, 116), (18, 111), (18, 112), (18, 113)], (23, 134),
                    (23, 135), (23, 136), (23, 137), (23, 138), (23, 139),
                    [(24, 140), (24, 141), (24, 142), (24, 143), (24, 144), (24, 145), (24, 146), (24, 147), (24, 148)],
                    [(22, 133)],
                    [(27, 153), (27, 154), (27, 155), (27, 156), (27, 157), (27, 158), (27, 159), (27, 160), (27, 161)],
                    [(28, 162), (28, 163), (28, 164), (28, 165), (28, 166), (28, 167)], [(31, 180), (31, 181)]]
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
ram1 = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
disk1 = Disk(PAGE_SIZE)
x = MMU_OPT(instructions1, ram1, disk1, order_to_unload1)
print(x.simulate())
