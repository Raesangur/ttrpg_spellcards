import json
import tkinter as tk
import tkinter.filedialog as fd
from enum import Enum
from fillpdf import fillpdfs
from pathlib import Path


abbrevs = {
    "Willpower" : "Will",
    "Reflex"    : "Ref",
    "Fortitude" : "Fort",

    "Acrobatics"   : "Accro",
    "Arcana"       : "Arcana",
    "Crafting"     : "Craft",
    "Deception"    : "Decept",
    "Diplomacy"    : "Diplo",
    "Intimidation" : "Intim",
    "Lore1"        : "Lore1",
    "Lore2"        : "Lore2",
    "Medicine"     : "Med",
    "Nature"       : "Nature",
    "Occultism"    : "Occult",
    "Performance"  : "Perf",
    "Religion"     : "Religion",
    "Society"      : "Society",
    "Stealth"      : "Stealth",
    "Survival"     : "Survival",
    "Thievery"     : "Thievery"
}

class Proficiency(Enum):
    UNTRAINED = 0
    TRAINED = 2
    EXPERT = 4
    MASTER = 6
    LEGENDARY = 8

def get_proficiency_bonus(charDict, proficiencyLevel):
    if proficiencyLevel == Proficiency.UNTRAINED:
        return 0

    level = int(charDict["level"])

    return level + proficiencyLevel.value


# Open file dialog and get 1 to n file paths
root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent = root, title = "Character sheets to load", filetypes=[("Portable Document Format", "*.pdf")])

# Iterate over character sheets
for cs in filez:
    characterName = Path(cs).stem
    print(characterName)
    newName = cs.replace(".pdf", "-new.pdf")

    with open("character-sheets/" + characterName + ".json", 'r') as charJson:
        # Load values from JSON
        charDict = json.load(charJson)
        print(charDict)
    
        # Get values currently in PDF
        ogCharDict = fillpdfs.get_form_fields(cs)
        print(ogCharDict)

        # Iterate over changes
        newCharDict = {}
        try:
            for val in charDict["Changes"]:
                # print(val)
                key = list(val.keys())[1]
                print(key)
                if val["Mode"] == "Edit":
                    newCharDict[key] = val[key]
                elif val["Mode"] == "Add":
                    newCharDict[key] = str(int(ogCharDict[key]) + int(val[key]))
                else:
                    printf("Invalid value " + val["Mode"])

        except:
            print("Invalid JSON (exiting):")
            print(charDict)
            exit()

        # Save copy of the character sheet with new values
        print(newCharDict)
        fillpdfs.write_fillable_pdf(cs, newName, newCharDict)
