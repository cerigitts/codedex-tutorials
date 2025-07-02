# This script retrieves & parses from a given URL to generate a hidden message.

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# SECTION 1: Request URL & Parse Grid Data from Google Doc
# ---------------------------------------------------------------

url = input("Enter the public Google Docs URL: ").strip()

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching the document: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.find_all('tr')

data = []
for row in table_rows[1:]:  # Skip header row
    cells = row.find_all('td')
    if len(cells) == 3:
        try:
            x = int(cells[0].text.strip())
            char = cells[1].text.strip()
            y = int(cells[2].text.strip())
            data.append((x, y, char))
        except ValueError:
            print("Skipping invalid row:", [c.text for c in cells])

print("\nParsed Coordinates:")
for entry in data:
    print(entry)

# ---------------------------------------------------------------
# SECTION 2: Generate Dynamic GRID from Parsed Data
# ---------------------------------------------------------------

max_x = max(entry[0] for entry in data)
max_y = max(entry[1] for entry in data)

grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

for x, y, char in data:
    flipped_y = max_y - y  # invert Y to correct visual orientation
    grid[flipped_y][x] = char

# ---------------------------------------------------------------
# SECTION 3: Display the Decoded Grid
# ---------------------------------------------------------------

print("\nDecoded Grid:\n")
for row in grid:
    print("".join(row))
