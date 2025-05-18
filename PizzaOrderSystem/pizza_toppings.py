

class Toppings:
    __slots__ = ['Name','OrderCode','Price']
    def __init__(self,code):
        self.Name = ""
        self.OrderCode = code
        self.Price = "0"

    def CheeseTopping(self):        #method to return a dictionary containing name, code and price of cheese only using ordere code 
        if self.OrderCode == "f":
            cheese={"self.Name":'Fresh Mozarella',"self.OrderCode":'f',"self.Price":1}
        elif self.OrderCode == "s":
            cheese={"self.Name":'Shredded Cheese',"self.OrderCode":'s',"self.Price":0.25}
        else:
            cheese={"self.Name":'Cheddar',"self.OrderCode":'c',"self.Price":0.5}
        return cheese

    def MeatToppings(self):         #method to return a dictionary containing name, code and price of meat or none only using order code 
        if self.OrderCode == "p":
            meat={"self.Name":'Pepperoni',"self.OrderCode":'p',"self.Price":1.5}
        elif self.OrderCode == "s":
            meat={"self.Name":'Sausage',"self.OrderCode":'s',"self.Price":1.5}
        elif self.OrderCode == "b":
            meat={"self.Name":'Bacon',"self.OrderCode":'b',"self.Price":1.0}
        elif self.OrderCode == "m":
            meat={"self.Name":'Meatball',"self.OrderCode":'m',"self.Price":2.0} 
        else:
            return None
        return meat

    def VegToppings(self):          #method to return a dictionary containing name, code and price of veggetables or none only using order code 
        if self.OrderCode == "m":
            veg={"self.Name":'Mushrooms',"self.OrderCode":'m',"self.Price":1.0}
        elif self.OrderCode == "b":
            veg={"self.Name":'Bell Peppers',"self.OrderCode":'b',"self.Price":1.0}
        elif self.OrderCode == "j":
            veg={"self.Name":'Jalapeno Peppers',"self.OrderCode":'j',"self.Price":1.0}
        elif self.OrderCode == "p":
            veg={"self.Name":'Pineapple',"self.OrderCode":'p',"self.Price":1.5}
        else:
            return None
        return veg

