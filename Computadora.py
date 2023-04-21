class Computer:
    # class attribute
    cores = 1
    instruc_sec = 1
    disk_access_tieme = 5  # segundos
    ram = 400  # kb

    # hard_disk=indefinido

    # instance attribute
    def __init__(self, name):
        self.name = name

    # instance method
    def specs(self):
        print(
            f"Las especificaciones de la computadora {self.name} son: \n ->Nucleos de procesamiento: {self.cores} \n ->Instrucciones por segundo: {self.instruc_sec} \n ->Tiempo de acceso al disco: {self.disk_access_tieme}s \n ->RAM: {self.ram}kb \n ->Memoria en disco ilimitada")


emu_computer = Computer("HP")

emu_computer.specs()
