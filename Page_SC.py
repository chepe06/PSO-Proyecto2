from Page import Page


class Page_SC(Page):
    def __init__(self, pid, ptr_id, page_id, direction, flag, size, loaded_time):
        super().__init__(pid, ptr_id, page_id, direction, flag, size, loaded_time)
        self.life = 1

    def __str__(self):
        text = "pid-" + str(self.pid) + "  page_id-" + str(self.page_id) + "  ptr_id-" + str(self.ptr_id) + \
               '  direction-' + str(self.direction) + "  flag-" + str(self.flag) + "  size-" + str(self.size) +\
               ' life-' + str(self.life) + "\n"
        return text

    def get_life(self):
        return self.life

    def set_life(self, life):
        self.life = life
