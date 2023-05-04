from Page import Page


class MMU:
    def __init__(self, ram, disk):
        self.RAM = ram
        self.disk = disk
        self.fragmentation = 0
        self.ptr_id = 1
        self.page_id = 1

        # MAPA DE MEMORIA
        self.memory_table = {}  # KEY -> PAGE_ID - VALUE -> PAGE()
        self.ptrs = {}          # KEY -> PTR_ID  - VALUE -> [PAGE_ID, ...]
        self.pids = {}          # KEY -> PID     - VALUE -> [PTR_ID , ...]

        self.simulation_time = 0
        self.thrashing = 0

    def get_memory_table(self):
        return self.memory_table

    def get_percent_ram_used(self):
        return (self.RAM.available_ram / self.RAM.total_ram) * 100

    def get_used_ram(self):
        return self.RAM.available_ram

    def get_percent_disk_used(self):
        return (self.disk.used_memory / self.RAM.total_ram) * 100
    

    def get_used_disk(self):
        return self.disk.used_memory

    def get_simulation_time(self):
        return self.simulation_time

    def get_thrashing(self):
        return self.thrashing

    def get_percent_thrashing(self):
        return (self.thrashing / self.simulation_time) * 100

    def get_fragmentation(self):
        return self.fragmentation

    def increment_page_id(self):
        self.page_id = self.page_id + 1

    def increment_ptr_id(self):
        self.ptr_id = self.ptr_id + 1

    def increment_fragmentation(self, size):
        self.fragmentation = self.fragmentation + size

    def decrement_fragmentation(self, size):
        self.fragmentation = self.fragmentation - size

    def increment_simulation_time(self):
        self.simulation_time = self.simulation_time + 1

    def increment_sim_thras_time(self):
        self.simulation_time = self.simulation_time + 5
        self.thrashing = self.thrashing + 5

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

    def create_page(self, pid, size):
        return Page(pid, self.ptr_id, self.page_id, -1, True, size)

    def add_page_to_memory_table(self, key, value):  # KEY -> PID - VALUE -> {} // KEY -> PTR - VALUE -> [ PAGE ID, ]
        temp = self.memory_table
        temp[key] = value
        self.memory_table = temp

    def delete_from_memory_table(self, page_id):
        temp = self.memory_table
        temp.pop(page_id)
        self.memory_table = temp

    def new(self, pid, size):
        pass

    def use(self, ptr_id):
        pass

    def delete(self, ptr_id):
        pass

    def kill(self, pid):
        pass

    def simulate(self, instruction):
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

        """
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
        """