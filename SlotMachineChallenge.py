# Slot Machine Challenge

import random

symbols = ['🍒','🍇','🍉','7️⃣']

def play():
    print("Welcome to the Slot Machine!")
    print("The Winning combination needed: 7️⃣ | 7️⃣ | 7️⃣")
    while True:
        play_game = input("Do you want to play? (y/n): ").lower()
        if play_game == 'y':
            results = random.choices(symbols, k=3)
            print(" | ".join(results))  # Join the results with a separator
            if results[0] == symbols[3] and results[1] == symbols[3] and results[2] == symbols[3]:
                print("Jackpot!💰")
            else:
                print("No Win, Thanks for playing!")
        elif play_game == 'n':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

play()