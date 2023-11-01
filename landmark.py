class landmark:
    def __init__(self, id, x, y):
        self.id = id
        self.X = x
        self.Y = y
        self.reached = False
        
    def __str__(self):
        return f"ID: {self.id}, position: {self.position}, type: {self.type}"   
    
class obstacle:
    def __init__(self, id, x, y):
        self.id = id
        self.X = x
        self.Y = y

    def updatePosition(self, x_offset, y_offset):
        self.X += x_offset
        self.Y += y_offset