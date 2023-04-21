class Page:
    def __init__(self, page_id, direction, flag):
        self.page_id = page_id
        self.direction = direction
        self.flag = flag

    # GETTERS
    def get_page_id(self):
        return self.page_id

    def get_direction(self):
        return self.direction

    def get_flag(self):
        return self.flag

    # SETTERS
    def set_page_id(self, id):
        self.page_id = id

    def set_direction(self, direction):
        self.direction = direction

    # TRUE -> MEMORIA REAL // FALSE -> MEMORIA VIRTUAL
    def set_flag(self, state):
        self.flag = state
