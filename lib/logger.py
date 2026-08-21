class Logger:
    def __init__(self):
        pass

    @staticmethod
    def d(*log: object):
        print("[DEBUG]: " + log)

    @staticmethod
    def e(*log: object):
        print("[!!ERROR]: " + log)