import pandas as pd


def charac_ok(user_input: str, df: pd.DataFrame) -> bool:
    """
    Check if the user entered any forbidden character.
    """
    string = user_input.replace(" ", "").upper()
    string_ok = True
    for charac in string:
        if not df.Character.isin([charac]).any():
            string_ok = False
            print(f"This character {charac} is not allowed.")
            break
    return string_ok


def clean_input(user_input: str) -> str:
    """Apply the .strip() and .upper functions to the user input"""
    return user_input.strip().upper()


def convert(user_input: str, df: pd.DataFrame):
    """
    Convert each character into its morse equivalent, and build a string made of morse codes.
    The convention is three spaces between letters, and seven spaces between words.
    """
    result = ""
    for charac in user_input:
        if charac == " ":
            # result.append("    ")
            result += "    "
        else:
            morse = df.Code.loc[df.Character == charac].values[0]
            result += morse
            # result.append(morse)
        # result.append("   ")
        result += "   "
    return result
