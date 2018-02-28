class LivingThing(object):
    """RPG-type character"""
    def __init__(self, name, health, magicPoints, inventory):
        self.name = name
        self._health = health
        self.magicPoints = magicPoints
        self.inventory = inventory
        self.hunger = 0  # all living things start with hunger level 0
        self.__age = 50

    def takeDamage(self, dmgAmount):
        self._health -= dmgAmount
        if self._health <= 0:
            self._health = 0
            print self.name + ' is dead!'
    
    def getAge(self):
        return self.__age

class Dragon(LivingThing):
    def __init__(self, name, health, magicPoints, inventory, wingspan):
        LivingThing.__init__(self, name, health, magicPoints, inventory)
        self._wingspan = wingspan
    

# Create the LivingThing object for the hero.
hero = LivingThing('Elsa', 50, 80, {})
monsters = []
monsters.append(LivingThing('Goblin', 20, 0, {'gold': 12, 'dagger': 1}))
monsters.append(LivingThing('Dragon', 300, 200, {'gold': 890, 'magic amulet': 1}))

print 'The hero {} has {} health.'.format(hero.name, hero._health)
print hero.getAge()

drogon = Dragon('Drogon', 20, 0, {'gold': 12, 'dagger': 1}, 100)


