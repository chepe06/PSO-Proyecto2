class MMU:
    def __init__(self):
        self.real_memory = 400
        self.table = {}

    def get_table(self):
        return self.table

    def update_table(self, key, value):  # KEY -> PID o puntero lógico ???// VALUE -> [ PAGE ID, ]
        temp = self.table
        temp[key] = value
        self.table = temp

    def new(self, pid, size):
        pass

    def use(self, ptr):
        pass

    def delete(self, ptr):
        pass

    def kill(self, pid):
        pass




