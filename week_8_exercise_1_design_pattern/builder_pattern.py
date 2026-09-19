class ProblemStatement:
    destination = None
    hotel = None
    transport = None
    meal_plan = None
    actiities = None
    insurance = None

    def __init__(self, destination, hotel, transport, meal_plan, activities, insurance):
        self.destination = destination
        self.hotel = hotel
        self.transport = transport
        self.meal_plan = meal_plan
        self.actiities = self.actiities
        self.insurance = insurance

    def __str__(self):
        return f'{self.__dict__}'


class ProblemBuilder:
    destination = None
    hotel = None
    transport = None
    meal_plan = None
    actiities = None
    insurance = None

    def setDestination(self, destination):
        self.destination = destination
        return self

    def setHotel(self, hotel):
        self.hotel = hotel
        return self

    def setTransport(self, transport):
        self.transport = transport
        return self

    def setMealPlan(self, meal_plan):
        self.meal_plan = meal_plan
        return self

    def setActivities(self, activities):
        self.actiities = self.actiities
        return self

    def setInsurance(self, insurance):
        self.insurance = insurance
        return self

    def build(self):
        return ProblemStatement(
            self.destination,
            self.hotel,
            self.transport, 
            self.meal_plan,
            self.actiities,
            self.insurance
        )


problem = (ProblemBuilder()
           .setDestination('Auckland')
           .setHotel('3-star')
           .setTransport('Flight')
           .setMealPlan('Breakfast')
           .setActivities('City Tower, Museum, Adventure Tour')
           .setInsurance('Yes')
           .build())
print(problem)
