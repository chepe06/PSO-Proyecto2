class Page:
    def __init__(self, page_id, direction, flag, size):
        self.page_id = page_id
        self.direction = direction
        self.flag = flag
        self.size = size

    def __str__(self):
        print("page_id- ")
        return str(self.page_id)

    # GETTERS
    def get_page_id(self):
        return self.page_id

    def get_direction(self):
        return self.direction

    def get_flag(self):
        return self.flag

    def get_size(self):
        return self.size

    # SETTERS
    def set_page_id(self, page_id):
        self.page_id = page_id

    def set_direction(self, direction):
        self.direction = direction

    # TRUE -> MEMORIA REAL // FALSE -> MEMORIA VIRTUAL
    def set_flag(self, state):
        self.flag = state

    def set_size(self, size):
        self.size = size
