############################################
#           decorator pattern
############################################
class Car:
    def __init__(self, cost):
        self._cost = cost

    def cost(self):
        return self._cost

class CarDecorator:
    def __init__(self, car):
        self.car = car

    def cost(self):
        return self.car.cost()

class GPSDecorator(CarDecorator):
    def cost(self):
        return self.car.cost() + 500

class SunroofDecorator(CarDecorator):
    def cost(self):
        return self.car.cost() + 1000

class LeatherSeatsDecorator(CarDecorator):
    def cost(self):
        return self.car.cost() + 1500

class PremiumSoundSystemDecorator(CarDecorator):
    def cost(self):
        return self.car.cost() + 800

car = PremiumSoundSystemDecorator(
    LeatherSeatsDecorator(
        SunroofDecorator(
            GPSDecorator(Car(25000))
        )
    )
)

print(f'Car costs ${car.cost()}')