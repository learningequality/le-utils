#!/usr/bin/env python3
import json
import os
import sys
from typing import Any
from typing import Dict
from typing import Optional

try:
    import langcodes
    import pycountry
except ImportError:
    print("Required libraries not found. Installing them now...")
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "langcodes[data]", "pycountry"]
    )
    import langcodes
    import pycountry


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save JSON data to a file with proper formatting."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"JSON data saved to {file_path}")


def _get_pycountry_language(code):
    language = pycountry.languages.get(alpha_2=code) or pycountry.languages.get(
        alpha_3=code
    )
    if not language:
        return {}
    data = {
        "code": language.alpha_2 if hasattr(language, "alpha_2") else language.alpha_3,
        "name": language.name,
    }
    if hasattr(language, "common_name"):
        data["native_name"] = language.common_name
    return data


def get_language_info(query: str) -> Optional[Dict[str, str]]:
    """Get language information using langcodes and pycountry."""
    # Try to parse as a language code first
    data = {}
    try:
        lang = langcodes.get(query) or langcodes.find(query)
    except LookupError:
        lang = None
    if not lang:
        return _get_pycountry_language(query) or None

    data["code"] = lang.to_tag()

    # Get the language name in English
    data["name"] = lang.display_name()

    # Try to get the native name
    data["native_name"] = lang.autonym() or data["name"]

    if data["native_name"] == data["name"]:
        data.update(_get_pycountry_language(data["code"]))

    return data


def main():
    # Get file path
    file_path = os.path.join(
        os.path.dirname(__file__), "../le_utils/resources/languagelookup.json"
    )

    # Load existing data
    data = load_json_file(file_path)
    if not data:
        print("Starting with an empty language dictionary.")
        data = {}
    else:
        print(f"Loaded {len(data)} language entries.")

    while True:
        query = input(
            "\nEnter language name or code to add (or press Enter to finish): "
        )
        if not query:
            break

        language_info = get_language_info(query)
        if language_info:
            code = language_info["code"]
            name = language_info["name"]
            native_name = language_info["native_name"]

            print("\nFound language information:")
            print(f"Code: {code}")
            print(f"Name: {name}")
            print(f"Native name: {native_name}")

            if code in data:
                print(
                    f"Warning: Language code '{code}' already exists in the data with the following information:"
                )
                print(f"Name: {data[code].get('name')}")
                print(f"Native name: {data[code].get('native_name')}")

            confirm = input("Add this language? (Y/N): ")
            if confirm.lower() == "y":
                data[code] = {"name": name, "native_name": native_name}
                print(f"Added language: {name}")
            else:
                print("Language not added.")
        else:
            print("Language not found. Please try a different query.")

    # Save the updated data
    if input("\nSave changes to the JSON file? (Y/N): ").lower() == "y":
        save_json_file(data, file_path)
    else:
        print("Changes not saved.")


if __name__ == "__main__":
    print("Language Manager: Add new languages to your JSON file")
    print("---------------------------------------------------")
    main()
    print("Program finished.")
