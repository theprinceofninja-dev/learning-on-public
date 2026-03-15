def __testfoo():
    print(f"Hello I am module level function")


_Class__testfoo = __testfoo


class Class:

    @staticmethod
    def __testfoo():
        print(f"Hello I am class level function")

    @classmethod
    def test(cls):
        # You access private function from functions that are inside the same class
        cls.__testfoo()
        # BUT HOW TO ACCESS MODULE LEVEL PRIVATE FUNCTIONS?
        __testfoo()  # This will be mangled automatically to _Class__testfoo


if __name__ == "__main__":
    # You can access the private function with a proxy
    Class.test()
    # You can access the private function with name mangling
    Class._Class__testfoo()
    # You can access the module level private function in the global scope
    __testfoo()
