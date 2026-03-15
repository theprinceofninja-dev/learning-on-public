class TestModule:
    public_member = None
    _protected_member = None
    __private_member = None

    def __init__(self):
        self.public_member = 'test'
        self._protected_member = 'test'
        self.__private_member = 'test'

    def print(self):
        print(self.public_member)
        print(self._protected_member)
        print(self.__private_member)