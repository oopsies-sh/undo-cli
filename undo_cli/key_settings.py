import os
import json

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".oopsies_data")

def prompt_user(prompt):
    return input(prompt)

def handle_openai_key(set_key=False):
    if set_key or not os.path.exists(SETTINGS_PATH):
        return prompt_for_key()

    try:
        with open(SETTINGS_PATH) as f:
            config = json.load(f)
        key = config.get("OPENAI_KEY")
        if not key:
            return prompt_for_key()
        return key
    except (ValueError, json.JSONDecodeError):
        return prompt_for_key()

def prompt_for_key():
    key = prompt_user("OpenAI Key > ")
    if not key:
        raise ValueError("OpenAI Key cannot be empty.")

    with open(SETTINGS_PATH, "w") as f:
        json.dump({"OPENAI_KEY": key}, f, indent=2)
    print("Settings Written")
    return key

def remove_openai_key():
    if os.path.exists(SETTINGS_PATH):
        os.remove(SETTINGS_PATH)
        print("OpenAI Key removed.")
    else:
        print("No OpenAI Key found.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Handle OpenAI Key")
    parser.add_argument("--setkey", action="store_true", help="Set a new OpenAI key")
    parser.add_argument("--removekey", action="store_true", help="Remove the OpenAI key")

    args = parser.parse_args()

    if args.removekey:
        remove_openai_key()
    else:
        key = handle_openai_key(args.setkey)
        if key:
            print(f"OpenAI Key: {key}")
        else:
            print("Failed to set or retrieve OpenAI Key.")