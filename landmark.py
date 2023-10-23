class landmark:
    def __init__(self, id, position, _type=None):
        self.id = id
        self.position = position
        self.type = _type
        self.reached = False

        
    def __str__(self):
        return f"ID: {self.id}, position: {self.position}, type: {self.type}"   