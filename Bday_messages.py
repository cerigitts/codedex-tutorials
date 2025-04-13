# This script generates a random birthday message from a predefined list.
# Used as module in the main.py

import random

def bd_messages():
    messages = ['Hope you have a very Happy Birthday! 🎈',
                'It\'s your special day – get out there and celebrate! 🎉',
                'You were born and the world got better – everybody wins! 🥳',
                'Have lots of fun on your special day! 🎂',
                'Another year of you going around the sun! 🌞']
    
    return random.choice(messages)

bd_messages()