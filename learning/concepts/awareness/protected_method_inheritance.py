def _testfoo(param):
    print(f"Hello I am module level function {param}")


class Class:

    @staticmethod
    def _testfoo(param):
        print(f"Hello I am class level function {param}")

    @classmethod
    def test(cls):
        _testfoo(cls)  # Hello I am module level function <class '__main__.Class'>
        cls._testfoo(cls)  # Hello I am class level function <class '__main__.Class'>


class Child(Class):
    @classmethod
    def test(cls):
        _testfoo(cls)  # Hello I am module level function <class '__main__.Child'>
        cls._testfoo(cls)  # Hello I am class level function <class '__main__.Child'>


class GrandChild(Class):
    @classmethod
    def test(cls):
        _testfoo(cls)  # Hello I am module level function <class '__main__.Child'>
        cls._testfoo(cls)  # Hello I am class level function <class '__main__.Child'>


if __name__ == "__main__":
    Class.test()
    Child.test()
    GrandChild.test()
