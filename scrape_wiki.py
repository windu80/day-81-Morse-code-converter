import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests

MORSE_WIKI_PAGE = 'https://en.wikipedia.org/wiki/Morse_code'
CSV_FILE_NAME = 'morse_code.csv'


def creating_morse_table() -> None:
    """
    Scrape the International Morse Code Table from the Wikipedia page, and save it as a .csv file
    """
    # USELESS
    # # Some headers necessary in the request, so we get an HTML page similar to if
    # # we were actually browsing from the browser
    # request_headers = {
    #     'Accept-Language': 'en-AU,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,de-DE;q=0.6,de;q=0.5,en-GB;q=0.4,en-US;q=0.3',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0'
    #                   ' Safari/537.36'
    # }

    # ----- Getting hold of the html page
    # response = requests.get(url=MORSE_WIKI_PAGE, headers=request_headers) # useless
    response = requests.get(url=MORSE_WIKI_PAGE)
    print("\nScraping the Morse Table from Wikipedia page...")
    print(f"Request response from Wikipedia: {response}")
    response.raise_for_status()
    print(f"Encoding detected: {response.encoding}\n")
    webpage = response.text

    # ----- Saving it the page, so I can check the HTML elements,
    # which somehow are different from the actual web version
    with open(file='saved_morse_wiki_page.html', mode='w', encoding='utf8') as file:
        file.write(webpage)

    # ----- Transforming it into soup, and getting the table elements
    print("Getting hold of the table...")
    soup = BeautifulSoup(webpage, "lxml")
    html_table = soup.find(name='table', class_='wikitable')
    column_names = [name.getText().strip() for name in html_table.find_all(name='th')]
    all_table_rows = html_table.find_all(name='tr')[1:]
    all_rows = []
    for tr in all_table_rows:
        # getting rid of the "hairspace" character "\u200a"
        row = [td.getText().strip().replace(u"\u200A", "") for td in tr.find_all(name='td')]
        all_rows.append(row)

    # ----- Writing the scraped data into a .CSV file
    print('Writing the Morse Table into a "morse_code.csv" file...')
    with open(file=CSV_FILE_NAME, mode='w', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(all_rows)

    # ----- Getting the data into a Pandas DataFrame and cleaning it up
    print("Cleaning up the Morse data table...")
    data = pd.read_csv(CSV_FILE_NAME)

    # Getting rid of the "Prosigns" category
    # So, keeping the Letters, Numbers, Punctuation and non-Latinextensions
    data = data.drop(index=data.loc[data.Category == 'Prosigns'].index)

    # Only keeping the upper case character (and rid of explanations and stuff)
    mask = data.loc[data.Category != 'Punctuation'].index
    data.loc[mask, 'Character'] = data.loc[data.Category != 'Punctuation'].Character.str[0]

    # Dealing with the punctuations
    mask = data.loc[(data.Category == 'Punctuation') & (data.Character.str.contains('[', regex=False))].index
    punctuations = data.loc[mask, 'Character'].str.split('[', expand=True, regex=False).iloc[:, 1].str[0]
    data.loc[mask, 'Character'] = punctuations
    data.iloc[42].Character = '('
    data.iloc[43].Character = ')'
    data.iloc[44].Character = '&'

    # Check if space characters
    # data.Code.str.contains(' ', regex=False))  # -> only morse code for A
    data.iloc[0].Code = data.iloc[0].Code.replace(" ", "")

    # ----- NOW WE HAVE THE PERFECT MORSE CONVERTER TABLE
    # Writing the cleaned table in the .csv file
    data.to_csv("morse_code.csv")
    print("Your Morse Table is already! You're all set to do some converting!")

    # Temporary view, so we can check if results alright
    # with pd.option_context('display.max_rows', 100):
    #     print(data)


