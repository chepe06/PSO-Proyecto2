from MMU import MMU

#from RAM import RAM
#from Disk import Disk


class MMU_FIFO(MMU):
    def __init__(self, ram, disk):
        super().__init__(ram, disk)
        self.queue = []

    def unload_page(self):
        page_to_unload = self.queue.pop(0)
        real_page = self.RAM.unload_page(page_to_unload.get_page_id())
        real_page.set_flag(False)
        real_page.set_loaded_time(-1)
        size = real_page.get_size()
        if size < self.RAM.page_size:
            self.decrement_fragmentation(self.RAM.page_size - size)
        self.add_page_to_memory_table(real_page.page_id,
                                      real_page)  # Se actualiza de la tabla de memoria
        self.disk.load_page(real_page)

    def new(self, pid, size):
        page_size = self.RAM.page_size
        pages = self.create_pages(pid, size, page_size)

        queue = []
        for i in range(len(pages)):

            if self.RAM.available_ram >= page_size:
                self.increment_simulation_time()  # HIT
                page_load = self.RAM.load_page(pages[i])
                queue.append(page_load)  # SE AGREGA A LA COLA
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria
            else:
                self.unload_page()
                self.increment_sim_thras_time()  # FAILURE
                page_load = self.RAM.load_page(pages[i])
                queue.append(page_load)  # SE AGREGA A LISTA TEMPORAL
                self.add_page_to_memory_table(page_load.page_id, page_load)  # Se agrega a la tabla de memoria

        [self.queue.append(p) for p in queue]  # SE AGREGA A LA COLA PRINCIPAL
        self.increment_ptr_id()

    def use(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for page_id in pages_in_ptr:
            if not page_id in pages_loaded:  # FAILURE
                self.increment_sim_thras_time()
                if self.RAM.available_ram < self.RAM.page_size:
                    self.unload_page()

                page_to_load = self.disk.unload_page(self.memory_table[page_id])
                page_to_load.set_flag(True)
                page_to_load.set_loaded_time(self.simulation_time)
                if page_to_load.get_size() < self.RAM.page_size:
                    self.increment_fragmentation(self.RAM.page_size - page_to_load.get_size())
                page_load = self.RAM.load_page(self.memory_table[page_id])
                self.queue.append(page_load)  # SE AGREGA A LA COLA
                self.add_page_to_memory_table(page_load.page_id,
                                              page_load)  # SE ACTUALIZA DE LA TABLA DE MEMORIA

            else:  # HIT
                self.increment_simulation_time()

    def delete(self, ptr_id):
        pages_in_ptr = self.ptrs[ptr_id]
        pages_loaded = [page.get_page_id() for page in self.RAM.memory if page.ptr_id == ptr_id]

        for p in pages_in_ptr:
            if p in pages_loaded:
                page_unloaded = self.RAM.unload_page(p)
                size = page_unloaded.get_size()
                if size < self.RAM.page_size:
                    self.decrement_fragmentation(self.RAM.page_size - size)
                # SE ELIMINA DE LA COLA
                self.queue.remove(page_unloaded)
            else:
                page_to_unload = self.memory_table[p]
                self.disk.unload_page(page_to_unload)
            self.delete_from_memory_table(p)

        self.ptrs.pop(ptr_id)

    def kill(self, pid):
        ptrs = self.pids[pid]
        for ptr_id in ptrs:
            if ptr_id in self.ptrs:
                self.delete(ptr_id)
        self.pids.pop(pid)


"""
# COMPUTER
TOTAL_RAM = 1000
AMOUNT_PAGES = 10
PAGE_SIZE = 100
RAM = RAM(TOTAL_RAM, AMOUNT_PAGES, PAGE_SIZE)
DISK = Disk(PAGE_SIZE)
MMU_FIFO = MMU_FIFO(RAM, DISK)

INSTRUCTIONS = [['new', '6', '842'], ['use', '1'], ['use', '1'], ['use', '1'], ['new', '3', '572'], ['new', '1', '301'], ['use', '2']]
#INSTRUCTIONS = [['new', '6', '842'], ['use', '1'], ['use', '1'], ['use', '1'], ['new', '3', '572'], ['new', '1', '301'], ['use', '2'], ['new', '3', '948'], ['delete', '4'], ['new', '10', '895'], ['use', '1'], ['use', '3'], ['kill', '1'], ['use', '1'], ['new', '5', '750'], ['kill', '10'], ['use', '1'], ['use', '1'], ['use', '6'], ['use', '1'], ['use', '6'], ['new', '8', '667'], ['use', '6'], ['use', '7'], ['use', '7'], ['use', '7'], ['kill', '6'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '7'], ['use', '6'], ['kill', '5'], ['new', '7', '840'], ['use', '7'], ['new', '4', '742'], ['use', '7'], ['use', '8'], ['use', '7'], ['use', '9'], ['new', '7', '254'], ['use', '9'], ['use', '9'], ['delete', '10'], ['use', '9'], ['new', '4', '704'], ['use', '7'], ['use', '11'], ['use', '7'], ['use', '11'], ['use', '11'], ['use', '7'], ['use', '7'], ['new', '8', '63'], ['use', '11'], ['use', '12'], ['use', '12'], ['use', '11'], ['use', '11'], ['new', '3', '899'], ['use', '11'], ['delete', '13'], ['new', '9', '503'], ['use', '14'], ['kill', '9'], ['new', '2', '313'], ['use', '12'], ['new', '2', '452'], ['use', '16'], ['use', '12'], ['use', '12'], ['new', '4', '110'], ['use', '12'], ['delete', '16'], ['use', '12'], ['use', '17'], ['use', '12'], ['use', '12'], ['use', '12'], ['use', '17'], ['use', '12'], ['use', '17'], ['use', '17'], ['new', '2', '733'], ['use', '17'], ['new', '8', '158'], ['use', '19'], ['kill', '8'], ['use', '18'], ['new', '7', '819'], ['use', '17'], ['use', '20'], ['use', '18'], ['use', '17'], ['use', '20'], ['use', '20'], ['use', '17'], ['use', '17'], ['use', '20'], ['use', '18'], ['new', '4', '412'], ['use', '18'], ['delete', '20'], ['use', '21'], ['use', '18'], ['use', '18'], ['new', '4', '71'], ['new', '2', '567'], ['use', '22'], ['new', '7', '893'], ['new', '7', '224'], ['use', '25'], ['use', '22'], ['use', '23'], ['kill', '2'], ['use', '25'], ['use', '22'], ['use', '25'], ['use', '25'], ['new', '3', '97'], ['use', '25'], ['use', '22'], ['use', '22'], ['use', '22'], ['use', '25'], ['use', '22'], ['use', '22'], ['use', '22'], ['kill', '7'], ['use', '26'], ['use', '26'], ['new', '4', '833'], ['use', '27'], ['use', '27'], ['delete', '26'], ['use', '27'], ['new', '4', '583'], ['use', '28'], ['new', '4', '613'], ['use', '29'], ['delete', '29'], ['new', '3', '437'], ['use', '30'], ['use', '30'], ['use', '30'], ['kill', '3'], ['new', '4', '178'], ['use', '31'], ['new', '4', '933'], ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['use', '32'], ['delete', '32'], ['new', '4', '328'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['use', '33'], ['kill', '4']]
#INSTRUCTIONS = [['new', '4', '12253'], ['use', '1'], ['use', '1'], ['new', '1', '16065'], ['new', '4', '6519'], ['new', '7', '1843'], ['new', '6', '7836'], ['new', '6', '8977'], ['new', '10', '16343'], ['new', '6', '14109'], ['new', '6', '16095'], ['new', '4', '9320'], ['use', '4'], ['new', '1', '12333'], ['new', '6', '2618'], ['use', '4'], ['new', '3', '5360'], ['new', '10', '10000'], ['new', '10', '16254'], ['new', '9', '16876'], ['delete', '13'], ['delete', '11'], ['new', '9', '16553'], ['new', '9', '11072'], ['new', '9', '11988'], ['use', '15'], ['new', '6', '11215'], ['new', '7', '6711'], ['kill', '4'], ['new', '7', '16667'], ['new', '3', '9137'], ['use', '22'], ['use', '22'], ['new', '5', '16200'], ['use', '24'], ['new', '7', '7557'], ['new', '9', '11190'], ['use', '24'], ['new', '1', '14306'], ['use', '26'], ['new', '8', '4766'], ['use', '20'], ['new', '8', '8561'], ['new', '6', '10941'], ['use', '30'], ['new', '8', '13112'], ['use', '30'], ['use', '15'], ['new', '8', '1442'], ['new', '1', '2581'], ['new', '3', '1807'], ['use', '15'], ['new', '5', '19268'], ['use', '32'], ['new', '6', '7471'], ['new', '5', '5629'], ['use', '25'], ['new', '1', '3296'], ['use', '32'], ['new', '3', '10274'], ['new', '2', '12811'], ['use', '15'], ['new', '1', '4646'], ['new', '2', '13872'], ['use', '37'], ['new', '8', '8426'], ['new', '5', '9050'], ['use', '44'], ['use', '42'], ['use', '42'], ['new', '1', '13293'], ['new', '9', '11714'], ['new', '10', '5365'], ['new', '1', '10410'], ['kill', '7'], ['new', '9', '12719'], ['use', '36'], ['new', '6', '12260'], ['new', '6', '6456'], ['new', '1', '5145'], ['new', '9', '9897'], ['new', '8', '4474'], ['use', '53'], ['new', '10', '6705'], ['new', '6', '15154'], ['use', '42'], ['new', '6', '15423'], ['use', '55'], ['new', '2', '5779'], ['new', '1', '10490'], ['new', '6', '17984'], ['use', '58'], ['use', '39'], ['new', '1', '2975'], ['new', '2', '6751'], ['use', '61'], ['use', '44'], ['new', '8', '5783'], ['use', '53'], ['use', '44'], ['use', '61'], ['new', '5', '3619'], ['use', '55'], ['new', '6', '6832'], ['new', '1', '14809'], ['new', '8', '19733'], ['new', '10', '13128'], ['delete', '62'], ['new', '2', '8701'], ['use', '65'], ['use', '69'], ['use', '69'], ['new', '3', '2530'], ['use', '67'], ['use', '53'], ['new', '2', '16445'], ['use', '70'], ['use', '68'], ['new', '3', '11202'], ['use', '64'], ['new', '8', '6685'], ['use', '65'], ['new', '1', '3360'], ['use', '68'], ['use', '74'], ['new', '5', '5130'], ['kill', '1'], ['new', '8', '3747'], ['use', '68'], ['new', '9', '17841'], ['new', '8', '17812'], ['use', '71'], ['new', '10', '5910'], ['use', '77'], ['use', '77'], ['use', '79'], ['use', '71'], ['use', '72'], ['new', '3', '19019'], ['use', '78'], ['new', '10', '14179'], ['new', '3', '17939'], ['new', '6', '19468'], ['use', '83'], ['use', '83'], ['use', '78'], ['use', '82'], ['use', '78'], ['use', '71'], ['use', '77'], ['use', '82'], ['kill', '2'], ['new', '10', '9144'], ['use', '82'], ['new', '6', '8611'], ['new', '8', '4028'], ['new', '3', '17448'], ['new', '9', '6317'], ['use', '88'], ['new', '9', '10090'], ['use', '87'], ['use', '89'], ['use', '85'], ['new', '6', '4976'], ['use', '86'], ['delete', '87'], ['use', '86'], ['use', '90'], ['use', '84'], ['use', '84'], ['use', '84'], ['use', '89'], ['new', '8', '9155'], ['use', '75'], ['use', '84'], ['use', '91'], ['use', '90'], ['use', '84'], ['new', '6', '5647'], ['use', '89'], ['use', '84'], ['new', '3', '13253'], ['new', '3', '10743'], ['new', '9', '10271'], ['use', '95'], ['use', '95'], ['new', '5', '9073'], ['new', '10', '2353'], ['use', '97'], ['use', '95'], ['new', '10', '17271'], ['use', '94'], ['use', '95'], ['use', '92'], ['use', '94'], ['use', '98'], ['new', '5', '5235'], ['use', '95'], ['delete', '98'], ['use', '92'], ['new', '10', '16256'], ['new', '5', '7822'], ['new', '3', '13533'], ['new', '8', '13343'], ['use', '100'], ['new', '10', '10714'], ['use', '102'], ['new', '3', '13172'], ['use', '95'], ['use', '104'], ['new', '10', '16740'], ['use', '103'], ['use', '103'], ['use', '95'], ['use', '95'], ['use', '105'], ['use', '103'], ['use', '106'], ['new', '9', '6944'], ['use', '107'], ['new', '5', '5617'], ['use', '92'], ['use', '107'], ['new', '10', '6673'], ['new', '9', '3887'], ['use', '110'], ['use', '110'], ['new', '9', '8814'], ['new', '9', '18005'], ['new', '8', '1171'], ['new', '8', '8309'], ['use', '108'], ['use', '108'], ['use', '92'], ['use', '108'], ['new', '9', '18520'], ['use', '115'], ['use', '114'], ['new', '8', '10320'], ['use', '116'], ['new', '9', '17393'], ['new', '8', '2812'], ['use', '109'], ['new', '8', '14800'], ['use', '119'], ['new', '3', '3057'], ['use', '108'], ['use', '120'], ['use', '117'], ['use', '108'], ['use', '109'], ['use', '119'], ['new', '3', '15417'], ['use', '92'], ['new', '5', '8748'], ['use', '109'], ['use', '109'], ['use', '119'], ['use', '109'], ['new', '8', '13088'], ['use', '122'], ['use', '109'], ['use', '121'], ['new', '6', '4586'], ['use', '122'], ['use', '124'], ['new', '8', '17480'], ['use', '124'], ['use', '117'], ['use', '124'], ['use', '109'], ['use', '117'], ['kill', '10'], ['use', '121'], ['use', '125'], ['new', '8', '12462'], ['use', '121'], ['use', '124'], ['new', '3', '7736'], ['kill', '5'], ['use', '124'], ['use', '126'], ['use', '126'], ['use', '117'], ['use', '124'], ['use', '126'], ['use', '117'], ['use', '124'], ['use', '126'], ['use', '126'], ['use', '117'], ['new', '6', '4420'], ['use', '127'], ['new', '8', '14034'], ['use', '129'], ['new', '9', '18426'], ['new', '6', '9899'], ['new', '3', '18264'], ['new', '9', '5241'], ['use', '129'], ['use', '133'], ['use', '131'], ['use', '133'], ['delete', '129'], ['use', '133'], ['use', '133'], ['use', '132'], ['new', '3', '18015'], ['use', '133'], ['use', '133'], ['use', '131'], ['use', '133'], ['new', '3', '3500'], ['use', '133'], ['use', '133'], ['use', '131'], ['use', '131'], ['new', '8', '6347'], ['use', '135'], ['use', '133'], ['use', '131'], ['new', '6', '4130'], ['use', '136'], ['use', '135'], ['use', '135'], ['new', '9', '7266'], ['use', '137'], ['new', '9', '9957'], ['use', '137'], ['new', '9', '8344'], ['use', '137'], ['delete', '135'], ['use', '137'], ['use', '140'], ['new', '9', '2476'], ['use', '141'], ['new', '8', '17017'], ['new', '3', '9496'], ['use', '143'], ['use', '143'], ['use', '143'], ['use', '141'], ['use', '142'], ['use', '137'], ['new', '6', '4976'], ['use', '143'], ['use', '144'], ['use', '141'], ['use', '144'], ['use', '141'], ['use', '143'], ['use', '144'], ['new', '9', '4828'], ['delete', '144'], ['use', '145'], ['use', '142'], ['use', '145'], ['use', '142'], ['delete', '142'], ['new', '3', '17182'], ['use', '146'], ['new', '9', '9614'], ['use', '146'], ['use', '147'], ['new', '6', '19137'], ['new', '3', '7839'], ['new', '6', '10776'], ['use', '149'], ['new', '9', '9760'], ['use', '149'], ['use', '149'], ['use', '149'], ['use', '150'], ['new', '3', '8035'], ['new', '9', '17146'], ['use', '152'], ['use', '153'], ['use', '152'], ['use', '153'], ['use', '150'], ['use', '153'], ['use', '150'], ['use', '152'], ['use', '153'], ['use', '152'], ['use', '153'], ['use', '152'], ['use', '150'], ['use', '150'], ['new', '6', '1365'], ['use', '153'], ['use', '154'], ['new', '9', '18758'], ['use', '155'], ['use', '152'], ['new', '6', '9288'], ['use', '152'], ['new', '8', '9600'], ['new', '9', '10073'], ['use', '152'], ['new', '8', '14503'], ['new', '8', '10845'], ['use', '152'], ['use', '152'], ['use', '152'], ['use', '152'], ['use', '156'], ['use', '152'], ['use', '152'], ['use', '156'], ['use', '152'], ['use', '156'], ['new', '3', '1759'], ['use', '160'], ['use', '156'], ['new', '8', '9521'], ['use', '162'], ['use', '161'], ['new', '9', '9003'], ['use', '162'], ['use', '163'], ['use', '163'], ['use', '163'], ['use', '163'], ['use', '163'], ['use', '161'], ['use', '156'], ['use', '162'], ['use', '162'], ['use', '163'], ['use', '162'], ['use', '161'], ['use', '163'], ['new', '6', '12823'], ['use', '164'], ['use', '161'], ['new', '9', '19003'], ['use', '164'], ['use', '164'], ['delete', '164'], ['use', '162'], ['use', '162'], ['new', '6', '3841'], ['kill', '9'], ['use', '161'], ['use', '161'], ['use', '166'], ['use', '166'], ['use', '162'], ['use', '166'], ['new', '3', '6574'], ['use', '167'], ['use', '166'], ['new', '3', '9743'], ['use', '166'], ['use', '162'], ['use', '166'], ['use', '168'], ['use', '162'], ['use', '166'], ['use', '166'], ['use', '168'], ['use', '162'], ['delete', '168'], ['use', '166'], ['use', '162'], ['use', '166'], ['use', '166'], ['use', '166'], ['use', '166'], ['use', '162'], ['use', '166'], ['use', '162'], ['use', '162'], ['use', '166'], ['use', '162'], ['new', '6', '1205'], ['use', '162'], ['use', '169'], ['use', '169'], ['use', '169'], ['use', '162'], ['use', '162'], ['use', '162'], ['new', '6', '7967'], ['use', '170'], ['kill', '6'], ['use', '162'], ['use', '162'], ['use', '162'], ['use', '162'], ['use', '162'], ['delete', '162'], ['new', '8', '6494'], ['use', '171'], ['use', '171'], ['use', '171'], ['use', '171'], ['use', '171'], ['new', '3', '12671']]
for x in INSTRUCTIONS:
    MMU_FIFO.simulate(x)
    print("\n QUEUE")
    [print(p) for p in MMU_FIFO.queue]
"""
