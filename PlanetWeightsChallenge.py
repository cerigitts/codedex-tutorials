# Codedex planet weights challenge

planet_name = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
planet_gravity = [0.38, 0.91, 1.00, 0.38, 2.34, 1.06, 0.92, 1.19]

# List out planet options for user clarity
print("Choose a planet by its number:")
for i, name in enumerate(planet_name, start=1):
    print(f"{i}. {name}")

# Use a loop to handle invalid entries gracefully
while True:
    try:
        planet_number = int(input('Enter the planet you want to know your weight on (1-8): '))
        if 1 <= planet_number <= 8:
            break
        else:
            print('Invalid planet number. Please enter a number between 1 and 8.')
    except ValueError:
        print('That’s not a valid number! Please enter a number between 1 and 8.')

earth_weight = float(input('Enter your weight in pounds: '))
planet_weight = earth_weight * planet_gravity[planet_number - 1]
print(f'Your weight on {planet_name[planet_number - 1]} is: {planet_weight}')