

import pizza_toppings as p                                      #imports pizza_toppings.py file as 'p' variable

class Pizza:                                                    #class to store pizza
    __slots__ = ['__Cheese','__Veggies','__Meat','__Price']
    def __init__(self):
        self.__Cheese = ""
        self.__Veggies = ""
        self.__Meat = ""
        self.__Price = 5.0

    def __str__(self):                                          #special method used when printing class which displays all the toppings
        return "One pizza with "+self.__Cheese+self.__Meat+self.__Veggies+": $"+str(self.__Price)

    def SetCheese(self,c):                                      #Mutator methods
        self.__Cheese = c
    def SetVeggies(self,v):
        self.__Veggies =  self.__Veggies + " ," + v
    def SetMeat(self,m):
        self.__Meat =  self.__Meat + " ," +  m
    def SetPrice(self,p):
        self.__Price = p + self.__Price

    def GetPrice(self):                                         #Accesor method
        return self.__Price
        
    def AddCheese(self,code,pizza):                             #method to add cheese on the pizza using pizza_toppings.py file
        topping = p.Toppings(code)
        cheese = topping.CheeseTopping()
        pizza.SetCheese(cheese["self.Name"])
        pizza.SetPrice(cheese["self.Price"])

    def AddVeggies(self,code,pizza):                            #method to add veggetables on the pizza using pizza_toppings.py file
        topping = p.Toppings(code)
        veggie = topping.VegToppings()
        if veggie != None:
            pizza.SetVeggies(veggie["self.Name"])
            pizza.SetPrice(veggie["self.Price"])
    
    def AddMeat(self,code,pizza):                               #method to add meat on the pizza using pizza_toppings.py file
        topping = p.Toppings(code)
        meat = topping.MeatToppings()
        if meat != None:
            pizza.SetMeat(meat["self.Name"])
            pizza.SetPrice(meat["self.Price"])
        