class Page:
    def __init__(self, pid, ptr_id, page_id, direction, flag, size, loaded_time):
        self.pid = pid
        self.ptr_id = ptr_id
        self.page_id = page_id
        self.direction = direction
        self.flag = flag
        self.size = size
        self.loaded_time = loaded_time

    def __str__(self):
        text = "pid-" + str(self.pid) + "  page_id-" + str(self.page_id) + "  ptr_id-" + str(self.ptr_id) + \
               '  direction-' + str(self.direction) + "  flag-" + str(self.flag) + "  size-" + str(self.size) + "\n"
        return text

    # GETTERS
    def get_pid(self):
        return self.pid

    def get_ptr_id(self):
        return self.ptr_id

    def get_page_id(self):
        return self.page_id

    def get_direction(self):
        return self.direction

    def get_flag(self):
        return self.flag

    def get_size(self):
        return self.size

    def get_loaded_time(self):
        return self.loaded_time
    # SETTERS

    def set_pid(self, pid):
        self.pid = pid

    def set_ptr_id(self, ptr_id):
        self.ptr_id = ptr_id

    def set_page_id(self, page_id):
        self.page_id = page_id

    def set_direction(self, direction):
        self.direction = direction

    def set_loaded_time(self, loaded_time):
        self.loaded_time = loaded_time

    # TRUE -> MEMORIA REAL // FALSE -> MEMORIA VIRTUAL
    def set_flag(self, state):
        self.flag = state

    def set_size(self, size):
        self.size = size
