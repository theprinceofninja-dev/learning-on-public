# Classes in python, basic

class Addition():
    #Member variables
    __a = 0
    __b = 0
    sum = 0
    #constructor
    def __init__(self,a,b):
        self.__a = a
        self.__b = b 
        self.test = "*******"
    def show(self):
        print(f"a={self.__a}, b={self.__b}, sum={self.sum}")
    def calculate(self):
        self.sum = self.__a+self.__b

my_add = Addition(5,6)
print(my_add.test)
my_add.show()
my_add.calculate()
my_add.show()
print("Hello World!")