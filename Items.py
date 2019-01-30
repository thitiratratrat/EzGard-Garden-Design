from abc import ABC, abstractmethod
class Plant:
    def __init__(self, name, region, spacing , water, price, imageParent, image):
        self.name = name
        self.spacing = spacing
        self.region = region
        self.water = water
        self.price = price
        self.imageParent = imageParent
        self.image = image
    def getName(self):
        return self.name
    def getSpacing(self):
        return self.spacing
    def getRegion(self):
        return self.region
    def getWater(self):
        return self.water
    def getPrice(self):
        return self.price

