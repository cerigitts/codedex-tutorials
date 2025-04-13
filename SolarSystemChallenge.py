# Solar System Challenge

from random import choice as ch
from math import pi

# Dictionary of planet radii (in km)
planet_radii = {
    'Mercury': 2440.0,
    'Venus': 6052.0,
    'Earth': 6371.0,
    'Mars': 3390.0,
    'Saturn': 58232.0
}

# Random planet selection
random_planet = ch(list(planet_radii.keys()))
r = planet_radii[random_planet]

# Calculate surface area
area = 4 * pi * r ** 2

# Output
print(f"The area of {random_planet} is {round(area, 2)} square kilometers.")
