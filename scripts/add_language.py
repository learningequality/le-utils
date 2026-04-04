#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

try:
    import langcodes
    import pycountry
except ImportError:
    print("Required libraries not found. Installing them now...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "langcodes[data]", "pycountry"])
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
    language = pycountry.languages.get(alpha_2=code) or pycountry.languages.get(alpha_3=code)
    if not language:
        return {}
    data = {
        "code": language.alpha_2 if hasattr(language, "alpha_2") else language.alpha_3,
        "name": language.name,
    }
    if hasattr(language, "common_name"):
        data["native_name"] = language.common_name
    return data


RTL_SCRIPTS = {"Arab", "Hebr", "Thaa", "Syrc", "Mand", "Samr", "Nkoo"}


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

    # Detect RTL from script
    try:
        script = lang.maximize().script
        if script in RTL_SCRIPTS:
            data["rtl"] = True
    except Exception:
        logging.warning("Could not detect script direction for %s", query)

    return data


def add_language(data, query, confirm=False):
    """Look up a language and add it to the data dict.

    Args:
        data: language dictionary to update
        query: language name or code to look up
        confirm: if True, prompt the user before adding

    Returns True if the language was added, False otherwise.
    """
    language_info = get_language_info(query)
    if not language_info:
        print(f"Language not found: {query}")
        return False

    code = language_info["code"]
    name = language_info["name"]
    native_name = language_info["native_name"]

    print(f"\nFound language: {code} - {name} ({native_name})")

    if code in data:
        print(f"Warning: '{code}' already exists: {data[code].get('name')} ({data[code].get('native_name')})")

    if confirm and input("Add this language? (Y/N): ").lower() != "y":
        print("Language not added.")
        return False

    entry = {"name": name, "native_name": native_name}
    if language_info.get("rtl"):
        entry["rtl"] = True
    data[code] = entry
    print(f"Added language: {name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Add languages to le_utils languagelookup.json")
    parser.add_argument(
        "languages",
        nargs="*",
        help="Language names or codes to add (non-interactive mode)",
    )
    args = parser.parse_args()

    # Get file path
    file_path = os.path.join(os.path.dirname(__file__), "../le_utils/resources/languagelookup.json")

    # Load existing data
    data = load_json_file(file_path)
    if not data:
        print("Starting with an empty language dictionary.")
        data = {}
    else:
        print(f"Loaded {len(data)} language entries.")

    added = 0
    if args.languages:
        # Non-interactive: add all specified languages and save
        for query in args.languages:
            if add_language(data, query):
                added += 1
    else:
        while True:
            query = input("\nEnter language name or code to add (or press Enter to finish): ")
            if not query:
                break
            if add_language(data, query, confirm=True):
                added += 1

        if input("\nSave changes to the JSON file? (Y/N): ").lower() != "y":
            return

    if added:
        save_json_file(data, file_path)
        print(f"\nAdded {added} language(s).")
    else:
        print("\nNo languages were added.")


if __name__ == "__main__":
    print("Language Manager: Add new languages to your JSON file")
    print("---------------------------------------------------")
    main()
    print("Program finished.")
