import math
from MMU import MMU
from RAM import RAM
from Disk import Disk


class MMM_OPT(MMU):
    def __init__(self, instructions, ram, disk, order_to_unload):
        super().__init__(instructions, ram, disk)
        self.order_to_unload = order_to_unload

    def new(self, pid, size):
        page_size = self.RAM.page_size
        pages = []
        if size > page_size:  # En caso de que se necesite más de una página
            pages_amount = math.ceil(size / page_size)
            fragmentation = (pages_amount * page_size) - size

            for i in range(pages_amount):
                size = size - page_size
                if size < page_size:
                    page = (pid, self.create_page(size))
                else:
                    page = (pid, self.create_page(page_size))
                pages.append(page)
                self.increment_page_id()

            self.increment_fragmentation(fragmentation)

        else:
            pages.append(self.create_page(size))
            self.increment_page_id()
            fragmentation = page_size - size
            self.increment_fragmentation(fragmentation)

        # self.relate_pid_to_ptrs(pid)  # Se relaciona el pid con el ptr

        for i in range(len(pages)):
            if self.RAM.available_ram >= page_size:
                self.RAM.load_page(pages[i])
            else:
                page_to_unload = self.order_to_unload.pop(0)
                print(page_to_unload)
                real_page = self.RAM.unload_page(page_to_unload)
                self.disk.load_page(real_page)

            page_id = pages[i]

        self.increment_ptr_id()

    def use(self, ptr):
        pass

    def delete(self, ptr):
        pass

    def kill(self, pid):
        pass

    def simulate(self):
        for instruction in self.instructions:
            if instruction[0] == "new":
                pid = int(instruction[1])
                size = int(instruction[2])
                self.new(pid, size)


instructions = [['new', '1', '400'], ['new', '1', '400'], ['new', '2', '400'], ['new', '2', '100'], ['use', '1'],
                ['use', '2'], ['new', '3', '500']]
order_to_unload = [(2, 5), (2, 6), (3, 9), (3, 10), (3, 11), (3, 12), (1, 1), (1, 2), (1, 3), (1, 4)]
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
ram = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
disk = Disk(PAGE_SIZE)
x = MMM_OPT(instructions, ram, disk, order_to_unload)
print(x.simulate())
