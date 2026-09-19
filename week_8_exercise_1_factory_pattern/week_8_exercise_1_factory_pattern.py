class Pizza:
    def prepare(self):
        print('ordered pizza')

class Burger:
    def prepare(self):
        print('ordered burger')

class Pasta:
    def prepare(self):
        print('ordered pasta')


class OrderFactory:
    @staticmethod
    def create(order):
        if order == 'pizza':
            return Pizza()
        elif order == 'burger':
            return Burger()
        elif order == 'pasta':
            return Pasta()

def main(xx):
    order = OrderFactory().create("pizza")
    order.prepare()


if __name__ == '__main__':
    main()