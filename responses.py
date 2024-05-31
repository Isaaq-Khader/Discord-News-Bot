from random import choice, randint

def get_response(user_input: str) -> str:
    formatted_response = user_input.lower()

    if formatted_response == "":
        return "No input given"
    elif "hello" in formatted_response:
        return "Hello there!"
    elif 'roll dice' in formatted_response:
        return f"You rolled: {randint(1, 6)}"
    else:
        return ""