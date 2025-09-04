class Item:
    def __init__(self, id: int = 0, ancho: int = 0, largo: int = 0):  # Constructor
        self.id = id
        self.ancho = ancho
        self.largo = largo

    def __str__(self):
        return f'Item #{self.id}: Ancho: {self.ancho} Largo: {self.largo}'