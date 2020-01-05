# pyramidcat types: water, lnswg (legume/nut/seed/whole grain), dairy, meal, veggie, fruit, meat, junk
# healthycat types: healthy, unhealthy, treat
# flavorcat types: sweet, savory, neither

# classification recommender system


class FoodType:
    def __init__(self, idx, name, pyramidcat, healthcat, flavorcat, notes):
        self.id = idx
        self.name = name
        self.pyramidcat = pyramidcat
        self.healthcat = healthcat
        self.flavorcat = flavorcat
        self.notes = notes
        self.pyramidict = {0: "water", 1: "lnswg", 2: "dairy", 3: "grain", 4: "veggie", 5: "fruit", 6: "meat", 7: "junk"}
        self.healthdict = {0: "healthy", 1: "unhealthy", 2: "treat"}
        self.flavdict = {0: "sweet", 1: "savory", 2: "neither"}
