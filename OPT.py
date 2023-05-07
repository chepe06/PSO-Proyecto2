import math


class OPT:
    def __init__(self, instructions, ram=1000, page_size=100):
        self.RAM = ram
        self.page_size = page_size
        self.ptr_id = 1
        self.page_id = 1
        self.pages_loaded = []  # (ptr, page_id)
        self.pages_in_disk = []  # (ptr, page_id)
        self.ptrs = {}  # key -> ptr_id ,  value ->  [page_id, ...]
        self.pids = {}  # key -> pid, value -> [ptr_id, ...]
        self.instructions = instructions  # [[command, data], ...]
        self.order_to_unload = []

    def increment_ptr_id(self):
        self.ptr_id = self.ptr_id + 1

    def increment_page_id(self):
        self.page_id = self.page_id + 1

    def decrease_ram(self, size):
        self.RAM = self.RAM - size

    def increase_ram(self, size):
        self.RAM = self.RAM + size

    def load_in_ram(self, ptr_id, page_id):
        temp = self.pages_loaded
        temp.append((ptr_id, page_id))
        self.pages_loaded = temp

    def load_in_disk(self, page):
        temp = self.pages_in_disk
        temp.append(page)
        self.pages_in_disk = temp

    def include_to_queue(self, page):
        temp = self.order_to_unload
        temp.append(page)
        self.order_to_unload = temp

    def relate_ptr_to_pages(self, page_id):
        if self.ptr_id in self.ptrs:
            temp = self.ptrs[self.ptr_id]
            temp.append(page_id)
            self.ptrs[self.ptr_id] = temp
        else:
            self.ptrs[self.ptr_id] = [page_id]

    def relate_pid_to_ptrs(self, pid):
        if pid in self.pids:
            temp = self.pids[pid]
            temp.append(self.ptr_id)
            self.pids[pid] = temp
        else:
            self.pids[pid] = [self.ptr_id]

    def page_to_unload(self, ptr_id, instructions):
        # PTR de las páginas cargadas
        ptr_page_loaded = []
        [ptr_page_loaded.append(page[0]) for page in self.pages_loaded
         if page[0] != ptr_id and page[0] not in ptr_page_loaded]

        # Instrucciones de uso sobre los ptrs que tiene páginas cargadas
        instructions_use = [int(ins[1]) for ins in instructions
                            if ins[0] == "use" and int(ins[1]) in ptr_page_loaded and int(ins[1]) != ptr_id]

        # print("PTR  PAGE LOADED", ptr_page_loaded)
        # print("INSTRUCTION USE", instructions_use)
        ptrs_next_use = []
        unload_complete = False

        for ptr_id in ptr_page_loaded:
            if ptr_id not in instructions_use:  # En caso de que no se use
                page_to_unload = [page for page in self.pages_loaded if page[0] == ptr_id][0]
                self.pages_loaded.remove(page_to_unload)  # Se baja la página de RAM
                self.pages_in_disk.append(page_to_unload)  # Se sube la página en Disco
                self.include_to_queue(page_to_unload)  # Se agrega a la cola de orden de bajar de RAM por el OTP
                self.increase_ram(self.page_size)  # Se aumenta la RAM en 1 tamaño de página
                unload_complete = True
                break
            else:  # Si se vuelve a usar se guarda la posición del siguiente uso
                index = instructions_use.index(ptr_id)
                ptrs_next_use.append(index)

        if not unload_complete:  # Se baja la página con el uso más lejano
            ptrs_next_use2 = ptrs_next_use.copy()
            ptrs_next_use2.sort(reverse=True)
            index = ptrs_next_use.index(ptrs_next_use2[0])
            page_to_unload = [page for page in self.pages_loaded if page[0] == instructions_use[index]][0]
            self.pages_loaded.remove(page_to_unload)  # Se baja la página de RAM
            self.pages_in_disk.append(page_to_unload)  # Se sube la página en Disco
            self.include_to_queue(page_to_unload)  # Se agrega a la cola de orden de bajar de RAM por el OTP
            self.increase_ram(self.page_size)  # Se aumenta la RAM en 1 tamaño de página

    def delete_ptr(self, ptr_id):
        pages = [(ptr_id, page) for page in self.ptrs[ptr_id]]
        for p in pages:
            if p in self.pages_loaded:
                self.pages_loaded.remove(p)
                self.increase_ram(self.page_size)
            else:
                self.pages_in_disk.remove(p)
        self.ptrs.pop(ptr_id)

    def kill_pid(self, pid):
        ptrs = self.pids[pid]
        for ptr in ptrs:
            if ptr in self.ptrs:
                self.delete_ptr(ptr)
        self.pids.pop(pid)

    def create_pages(self, pages_amount):
        pages = []
        for i in range(pages_amount):
            pages.append(self.page_id)
            self.increment_page_id()
        return pages

    def process_commands(self):
        ins = 0
        for instruction in self.instructions:
            if instruction[0] == "new":
                pid = int(instruction[1])
                size = int(instruction[2])

                if size > self.page_size:  # En caso de que se necesite más de una página
                    pages_amount = math.ceil(size / self.page_size)

                    pages = self.create_pages(pages_amount)
                else:
                    pages = self.create_pages(1)

                self.relate_pid_to_ptrs(pid)  # Se relaciona el pid con el ptr

                for i in range(len(pages)):
                    if self.RAM >= self.page_size:
                        self.decrease_ram(self.page_size)
                    else:
                        instruction2 = self.instructions[ins:].copy()
                        self.decrease_ram(self.page_size)
                        self.page_to_unload(self.ptr_id, instruction2)

                    page_id = pages[i]
                    self.load_in_ram(self.ptr_id, page_id)
                    self.relate_ptr_to_pages(page_id)  # Se relaciona el ptr con el page_id

                self.increment_ptr_id()

            elif instruction[0] == "use":
                ptr_id = int(instruction[1])
                pages_in_ptr = self.ptrs[ptr_id]
                pages_loaded = [page[1] for page in self.pages_loaded if page[0] == ptr_id]

                for page in pages_in_ptr:
                    if not page in pages_loaded:
                        if self.RAM >= self.page_size:
                            self.decrease_ram(self.page_size)
                            self.load_in_ram(ptr_id, page)
                            self.pages_in_disk.remove((ptr_id, page))  # REVISAR
                        else:
                            instruction2 = self.instructions[ins:].copy()
                            self.decrease_ram(self.page_size)
                            self.page_to_unload(ptr_id, instruction2)
                            self.load_in_ram(ptr_id, page)
                            self.pages_in_disk.remove((ptr_id, page))

            elif instruction[0] == "delete":
                ptr_id = int(instruction[1])
                self.delete_ptr(ptr_id)

            elif instruction[0] == "kill":
                pid = int(instruction[1])
                self.kill_pid(pid)

            ins = ins + 1
            """
            print("INSTRUCTION", instruction)
            print("PID -> PTRS", x.pids)
            print("PTR -> PAGES", x.ptrs)
            print("RAM", x.RAM)
            print("PAGES LOADED", x.pages_loaded)
            print("PAGES IN DISK ", x.pages_in_disk)
            print("ORDER TO UNLOAD", x.order_to_unload)
            print("\n")
            """

        return self.order_to_unload


def open_document(filename):
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            instruction = line.split("(")
            if instruction[0] == "new":
                data = instruction[1].split(",")
                instruction[1] = data[0]
                if data[1][-1] == "\n":
                    instruction.append(data[1][:-2])
                else:
                    instruction.append(data[1][:-1])
            elif instruction[0] == "use" or instruction[0] == "delete" or instruction[0] == "kill":
                if instruction[1][-1] == "\n":
                    instruction[1] = instruction[1][:-2]
                else:
                    instruction[1] = instruction[1][:-1]
            instructions.append(instruction)

    return instructions

"""
instructions = open_document("generatedFile.txt")
print(instructions)

x = OPT()
print(x.process_commands())
print(x.instructions)"""