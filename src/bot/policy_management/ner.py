class NER:
    def __init__(self, type, values, tag):
        self.type = type
        self.values = values
        self.tag = tag
    
    def __init__(self, type, values):
        self.type = type
        self.values = values
        self.tag = None
    
    
    def __init__(self):
        self.type = None
        self.values = []
        self.tag = None