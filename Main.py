# This script calculates the number of days until the next birthday and displays a birthday message if today is the birthday.
# Uses the bday_messages module to get a random birthday message.

import datetime
import bday_messages

today = datetime.date.today()
my_birthday = datetime.date(1980, 6, 15)  # Replace with your actual birthdate

# Extract the birthday month and day
bday_month = my_birthday.month
bday_day = my_birthday.day

# Determine the year of the next birthday
if (today.month, today.day) > (bday_month, bday_day):
    next_birthday = datetime.date(today.year + 1, bday_month, bday_day)
else:
    next_birthday = datetime.date(today.year, bday_month, bday_day)

# Calculate how many days away it is
days_away = (next_birthday - today).days

# Output
if days_away == 0:
    print("Happy Birthday! 🎂")
    print(f"Your birthday message is: {bday_messages.bd_messages()}")
else:
    print(f"Your birthday is in {days_away} day(s).")
