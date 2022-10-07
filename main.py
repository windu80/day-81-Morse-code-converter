import pandas as pd
from scrape_wiki import creating_morse_table
from input_treatment import charac_ok, clean_input, convert

# ----- 1. Checking if Morse Reference table exists
try:
    data = pd.read_csv('morse_code.csv')
    test_access = data.iloc[15]
except (FileNotFoundError, pd.errors.EmptyDataError, IndexError):
    creating_morse_table()
    data = pd.read_csv('morse_code.csv')

# ----- 2. User Interface
with open(file='welcome_ASCII_art.txt', mode='r') as file:
    content = file.read()
    print(content)
user_input = input("Please enter a word or a phrase you would like to convert into Morse Code:\n")

# Checking if no forbidden characters
while not charac_ok(user_input, data):
    user_input = input("Please enter a word or a phrase again:\n")

# ----- 3. Converting
print("\nThis is your phrase in Morse Code! :) ")
print(convert(clean_input(user_input), data))

# Temporary view, so we can check if results alright
# with pd.option_context('display.max_rows', 100):
#
#     print(data.Character)
