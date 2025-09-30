class Item:
    def __init__(self, id: int = 0, dem: int = 0, ancho: int = 0, largo: int = 0):  # Constructor
        self.id = id
        self.ancho = ancho
        self.largo = largo
        self.dem = dem

    def __str__(self):
        return f'Item #{self.id}: Ancho: {self.ancho} Largo: {self.largo}'


class Solution:
    def __init__(self):  # Constructor
        self.dem_com = {}  # Demanda completada
        self.dem_fal = {}  # Demanda faltante
        self.desperdicio = 0.0  # Desperdicio final
        self.fitness = 0  # Puntuación de que tan buena es la solución
        self.matrixes = []  # Guardar los cortes de la solución para la representación gráfica
        self.permutation: list[Item] = []  # Guardar los cortes de la solución para la representación gráfica

    def __str__(self):
        pass

    def to_dict(self):
        pass
