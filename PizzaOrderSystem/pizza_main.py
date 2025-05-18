

import pizza as p                               #imports pizza.py file as 'p' variable

def PrintCheeseDetails():                       #function that prints all the details for cheeses available, upon call
    print("Cheese Options: \n")
    print("Fresh Mozzarella(f): $1.0  Shredded Cheese(s): $0.25  Cheddar(c): $0.5")

def PrintMeatDetails():                         #function that prints all the details for meats available, upon call
    print("Meat Options: \n")
    print("Pepperoni(p): $1.5  Sausage(s): $1.5  Bacon(b): $1.0  Meatball(m): $2.0  None(n): $0.0")

def PrintVeggieDetails():                       #function that prints all the vegetables available, upon call
    print("Veggie Options: \n")
    print("Mushrooms(m): $1.0  Bell Peppers(b): $1.0  Jalapeno Peppers(j): $1.0  Pineapple(p): $1.5  None(n): $0.0")

def MakePizza(Pizza1):                                                  #function that makes the pizza using pizza.py file and returns price
    cheese = input("Choose one type of cheese(0 for options): ")
    if cheese == "0":
        PrintCheeseDetails()
        cheese = input("Choose one type of cheese(0 for options): ")
    Pizza1.AddCheese(cheese,Pizza1)
    meat = input("Choose your meats (0 for options): ")
    if meat == "0":
        PrintMeatDetails()
        meat = input("Choose your meats (0 for options): ")
    for word in meat:
        if word!= " ":
            Pizza1.AddMeat(word,Pizza1)
    veggie = input("Choose your veggies (0 for options): ")
    if veggie == "0":
        PrintVeggieDetails()
        veggie = input("Choose your veggies (0 for options): ")
    for word in veggie:
        if word!= " ":
            Pizza1.AddVeggies(word,Pizza1)
    total = Pizza1.GetPrice()
    return total
    

def main():                                                                     #main function
    Pizza1 = p.Pizza()
    Pizza2 = p.Pizza()
    print("Welcome to Pizza Factory, where all orders include two pizzas!\n","\nFor your first pizza\n")
    total = MakePizza(Pizza1)                                               
    print("\nFor your second Pizza\n")
    total = MakePizza(Pizza2) + total                                           #adds the total costs of the two pizzas
    print("Your order is :\n")
    print(Pizza1)
    print(Pizza2)
    print("Total due: $",total)

main()
