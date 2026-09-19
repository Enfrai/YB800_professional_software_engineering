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



#######################################################

class Button(ABC):
    @abstractmethod
    def draw(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def draw(self):
        pass

class WindowsButton(Button):
    def draw(self):
        print('A windows button drawn.')

class WindowsCheckbox(Checkbox):
    def draw(self):
        print('A windows checkbox drawn.')

class MacButton(Button):
    def draw(self):
        print('A mac button drawn.')

class MacCheckbox(Checkbox):
    def draw(self):
        print('A mac checkbox drawn.')


class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_checkbox(self):
        return MacCheckbox()

    def create_button(self):
        return MacButton()

#######################################################

def main():
    order = OrderFactory().create("pizza")
    order.prepare()

    SMSFactory().create_notification().notify()

    MacFactory().create_button().draw()


if __name__ == '__main__':
    main()
