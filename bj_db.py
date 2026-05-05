import re
import pandas as pd

# Load your extracted text from the PDF
with open('tests for 5000 deals by 10000 trials.txt', 'r') as file:
    lines = file.readlines()

# Prepare storage
data = []

current_deal = None
pimc_hands = None
pimc_wins = None
basic_hands = None
basic_wins = None

# Loop through each line
for line in lines:
    line = line.strip()

    # Check if it's a deal completion line
    if line.startswith("--- Completed"):
        match = re.search(r'Completed (\d+)/\d+ Deals', line)
        if match:
            current_deal = int(match.group(1))

    # Check if it's a PIMC line
    elif line.startswith("PIMC -> Hands:"):
        numbers = re.findall(r'\d+', line)
        if len(numbers) >= 3:
            pimc_hands = int(numbers[0])
            pimc_wins = int(numbers[2])

    # Check if it's a Basic Strategy line
    elif line.startswith("Basic Strategy -> Hands:"):
        numbers = re.findall(r'\d+', line)
        if len(numbers) >= 3:
            basic_hands = int(numbers[0])
            basic_wins = int(numbers[2])

        # Now, after reading Basic Strategy, we have a full set: save the record
        if current_deal is not None and pimc_hands is not None and basic_hands is not None:
            data.append({
                'Deals Played': current_deal,
                'PIMC Hands': pimc_hands,
                'PIMC Wins': pimc_wins,
                'Basic Hands': basic_hands,
                'Basic Wins': basic_wins
            })
            # Reset temporary variables for next block
            current_deal = None
            pimc_hands = None
            pimc_wins = None
            basic_hands = None
            basic_wins = None

# Make the DataFrame
df = pd.DataFrame(data)

# Add Win Rate Columns
df['PIMC Win Rate'] = df['PIMC Wins'] / df['PIMC Hands']
df['Basic Win Rate'] = df['Basic Wins'] / df['Basic Hands']

# Show the table
print(df)

# Save if you want
df.to_csv('win_rates_table_4.csv', index=False)