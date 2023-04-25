class OPT:
    def __init__(self, document_name):
        self.document_name = document_name
        self.RAM = 2000
        self.ptr_id = 1
        self.ptrs_loaded = {}  # key -> ptr_id ,  value ->  size
        self.ptrs_in_disk = {}  # key -> ptr_id ,  value ->  size
        self.pids = {}  # key -> pid, value -> ptr_id
        self.instructions = self.open_document()  # [[command, data], ...]
        self.order_to_unload = []

    def increment_ptr_id(self):
        self.ptr_id = self.ptr_id + 1

    def decrease_ram(self, size):
        self.RAM = self.RAM - size

    def increase_ram(self, size):
        self.RAM = self.RAM + size

    def load_in_ram(self, size):
        self.ptrs_loaded[self.ptr_id] = size

    def load_in_ram2(self, ptr_id, size):
        self.ptrs_loaded[ptr_id] = size

    def load_in_disk(self, ptr_id, size):
        self.ptrs_in_disk[ptr_id] = size

    def include_to_queue(self, ptr_id):
        temp = self.order_to_unload
        temp.append(ptr_id)
        self.order_to_unload = temp

    def relate_pid_to_ptrs(self, pid):
        if pid in self.pids:
            temp = self.pids[pid]
            temp.append(self.ptr_id)
            self.pids[pid] = temp
        else:
            self.pids[pid] = [self.ptr_id]

    def ptr_to_unload(self, instructions, needed_size):
        instructions_use = [int(ins[1]) for ins in instructions if ins[0] == "use"]
        ptrs_loaded_keys = list(self.ptrs_loaded.keys())
        ptrs_next_use = []
        unload_complete = False

        for ptr_id in ptrs_loaded_keys:
            if ptr_id not in instructions_use:  # Si no se vuelve a usar
                size = self.ptrs_loaded[ptr_id]
                self.ptrs_loaded.pop(ptr_id)  # Se baja de RAM
                self.load_in_disk(ptr_id, size)  # Se sube a disco
                self.include_to_queue(ptr_id)  # Se agrega a la cola de orden de bajar de RAM por el OTP
                self.increase_ram(size)
                needed_size = needed_size - size
                if self.RAM > needed_size:
                    unload_complete = True
                    break

            else:  # Si se vuelve a usar se guarda la posición del siguiente uso

                index = instructions_use.index(ptr_id)
                ptrs_next_use.append(index)

        if not unload_complete:
            ptrs_next_use2 = ptrs_next_use.copy()
            ptrs_next_use2.sort(reverse=True)
            index2 = ptrs_loaded_keys.index(ptrs_next_use2[0])
            ptr_id2 = ptrs_loaded_keys[index2]
            size2 = self.ptrs_loaded[ptr_id2]

            self.ptrs_loaded.pop(ptr_id2)  # Se baja de RAM
            self.load_in_disk(ptr_id2, size2)  # Se sube a disco
            self.include_to_queue(ptr_id2)  # Se agrega a la cola de orden de bajar de RAM por el OTP
            self.increase_ram(size2)

            needed_size = needed_size - size2

            i = 1
            while self.RAM < needed_size:
                index2 = ptrs_next_use.index(ptrs_next_use2[i])
                ptr_id2 = ptrs_loaded_keys[index2]
                size2 = self.ptrs_loaded[ptr_id2]
                self.ptrs_loaded.pop(ptr_id2)  # Se baja de RAM
                self.include_to_queue(ptr_id2)  # Se agrega a la cola de orden de bajar de RAM por el OTP
                self.increase_ram(size2)
                i = i + 1
                needed_size = needed_size - size2

    def open_document(self):
        instructions = []
        with open(self.document_name, "r") as file:
            for line in file:
                instruction = line.split("(")
                if instruction[0] == "new":
                    data = instruction[1].split(",")
                    instruction[1] = data[0]
                    instruction.append(data[1][:-2])
                else:
                    instruction[1] = instruction[1][:-2]  # AGREGAR SALTO DE LINEA AL FINAL DEL DOCUMENTO
                instructions.append(instruction)
        return instructions

    def process_commands(self):
        ins = 0
        for instruction in self.instructions:
            if instruction[0] == "new":
                pid = instruction[1]
                size = int(instruction[2])
                if self.RAM >= size:
                    self.decrease_ram(size)
                    self.load_in_ram(size)
                    self.relate_pid_to_ptrs(pid)
                else:
                    instruction2 = self.instructions[ins:].copy()
                    self.ptr_to_unload(instruction2, size)
                    self.decrease_ram(size)
                    self.load_in_ram(size)
                    self.relate_pid_to_ptrs(pid)

                self.increment_ptr_id()

            elif instruction[0] == "use":
                ptr_id = int(instruction[1])
                if not ptr_id in self.ptrs_loaded:
                    size = self.ptrs_in_disk[ptr_id]
                    if self.RAM >= size:
                        self.decrease_ram(size)
                        self.load_in_ram2(ptr_id, size)
                    else:
                        instruction2 = self.instructions[ins].copy()
                        self.ptr_to_unload(instruction2, size)
                        self.decrease_ram(size)
                        self.load_in_ram2(ptr_id, size)
        ins = ins + 1
        print("PIDS", self.pids)
        print("PTRS-LOADED", self.ptrs_loaded)
        print("RAM", self.RAM)
        print("ORDER TO UNLOAD", self.order_to_unload)


x = OPT('Test.txt')
x.process_commands()
