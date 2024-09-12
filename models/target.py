class Target:
    def __init__(self, city, priority):
        self.city = city
        self.priority = priority

    def __repr__(self):
        return f"city: {self.city}, priority: {self.priority}"