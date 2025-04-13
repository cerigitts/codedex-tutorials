# Drive-Thru Menu Program
# This program displays a menu and allows the user to select an item by number.

menu = ['🍔 Cheeseburger','🍟 Fries','🥤 Soda','🍦 Ice Cream','🍪 Cookie']

def get_item(x):
    return menu[x-1]

def welcome():
  print("Welcome to the Drive-Thru!")
  print("Here's the menu:")
  for i, name in enumerate(menu, start=1):
    print(f"{i}. {name}")

welcome()

option = int(input('What would you like to order? '))
print(get_item(option))