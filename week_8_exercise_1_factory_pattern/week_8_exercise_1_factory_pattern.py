from abc import ABC, abstractmethod

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

#######################################################

class NotificationMethod(ABC):
    @abstractmethod
    def notify(self):
        pass

class Email(NotificationMethod):
    def notify(self):
        print('through email')

class SMS(NotificationMethod):
    def notify(self):
        print('through sms')

class Push(NotificationMethod):
    def notify(self):
        print('through push')

class NotificationFactory(ABC):
    @abstractmethod
    def create_notification(self):
        pass

class EmailFactory(NotificationFactory):
    def create_notification(self):
        return Email()

class SMSFactory(NotificationFactory):
    def create_notification(self):
        return SMS()

class PushFactory(NotificationFactory):
    def create_notification(self):
        return Push()
    

#######################################################

def main():
    order = OrderFactory().create("pizza")
    order.prepare()

    push = SMSFactory()
    push.create_notification().notify()


if __name__ == '__main__':
    main()