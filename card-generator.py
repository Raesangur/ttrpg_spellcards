import json
import os
import re
import subprocess

def check_spell_components(card):
    # Check Spell Traits
    if "spell-traits" in card:
        card["has-spell-traits"] = "-"
    else:
        card["has-spell-traits"] = ""

    # Check Spell Heightening
    if "spell-heightened-level0" in card:
        card["has-heightened0"] = ""
    else:
        card["has-heightened0"] = "%"

    if "spell-heightened-level1" in card:
        card["has-heightened1"] = ""
    else:
        card["has-heightened1"] = "%"

    if "spell-heightened-level2" in card:
        card["has-heightened2"] = ""
    else:
        card["has-heightened2"] = "%"

    if "spell-heightened-level3" in card:
        card["has-heightened3"] = ""
    else:
        card["has-heightened3"] = "%"

    # Check Spell Actions
    if "spell-action-title" in card:
        card["has-spell-action"] = ""
    else:
        card["has-spell-action"] = "%"

    if "spell-action-trigger" in card:
        card["has-spell-action-trigger"] = ""
    else:
        card["has-spell-action-trigger"] = "%"

    # Check Saving Throws
    if "spell-saving-critical-success" in card:
        card["has-saving-cs"] = ""
    else:
        card["has-saving-cs"] = "%"

    if "spell-saving-success" in card:
        card["has-saving-s"] = ""
    else:
        card["has-saving-s"] = "%"

    if "spell-saving-failure" in card:
        card["has-saving-f"] = ""
    else:
        card["has-saving-f"] = "%"

    if "spell-saving-critical-failure" in card:
        card["has-saving-cf"] = ""
    else:
        card["has-saving-cf"] = "%"


def make_spell_tags(card):
    existing_tags = {"spell-duration": "Duration",
                     "spell-saving-throw": "Saving Throw",
                     "spell-targets": "Target",
                     "spell-trigger": "Trigger",
                     "spell-area": "Area"}
    tags = [tag for tag in existing_tags.keys() if tag in card.keys()]
    count = len(tags)
    print("count: " + str(count) + " from tags: " + str(tags))

    if count > 3:
        print("Too many tags!")

    elif count == 1:
        card["spell-tag0"] = ""
        card["spell-tag2"] = ""
        card["spell-tag1"] = existing_tags[tags[0]]
        card["spell-value0"] = ""
        card["spell-value1"] = ""
        card["spell-value1"] = card[tags[0]]

    elif count == 2:
        card["spell-tag1"] = ""
        card["spell-tag0"] = existing_tags[tags[0]]
        card["spell-tag2"] = existing_tags[tags[1]]
        card["spell-value0"] = card[tags[0]]
        card["spell-value2"] = card[tags[1]]

    elif count == 3:
        card["spell-tag0"] = existing_tags[tags[0]]
        card["spell-tag1"] = existing_tags[tags[1]]
        card["spell-tag2"] = existing_tags[tags[2]]
        card["spell-value0"] = card[tags[0]]
        card["spell-value1"] = card[tags[1]]
        card["spell-value2"] = card[tags[2]]



def process_hero_cards():
    with open("hero-template.tex", 'r') as inputF: 
        template = inputF.read()

        with open("hero-cards.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                spaces = card["hero-title"].count(' ')
                title = card["hero-title"].replace(' ', '_')

                if title + ".pdf" in os.listdir("output"):
                    print(title + " already exists, skipping...")
                    continue

                spacing  = "10mm" if len(title) < (17 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"
                spacing2 =  3 if len(title) < (13 + spaces) else 9 if len(title) < (29 + spaces) else 13
                spacing2 += 9 if len(card["hero-trigger"]) > 90 else 6 if len(card["hero-trigger"]) > 60 else 0
                spacing2 = str(spacing2) + "mm"

                text = template.replace("hero-title", card["hero-title"])
                text = text.replace("hero-type", card["hero-type"])
                text = text.replace("hero-trigger", card["hero-trigger"])
                text = text.replace("hero-description", card["hero-description"])
                text = text.replace("hero-fortune", "This is a Fortune effect" if "Fortune" in card["hero-type"] else "")
                #text = text.replace("hero-spacing-secondary", "2mm")
                text = text.replace("hero-spacing-secondary", spacing2)
                text = text.replace("hero-spacing",  spacing)

                outputF = open("output/hero-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/hero-" + title + ".tex -output-directory=output -job-name=" + title)

def process_spell_cards():
    with open("spell-template.tex", 'r') as inputF: 
        template = inputF.read()

        with open("spell-cards.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                spaces = card["spell-name"].count(' ')
                title = card["spell-name"].replace(' ', '_').lower()

                if "spell-" + title + ".pdf" in os.listdir("output"):
                    print(title + " already exists, skipping...")
                    continue

                spacing  = "10mm" if len(title) < (17 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"

                check_spell_components(card)
                make_spell_tags(card)

                def get(string):
                    return card.get(string, "")

                text = template.replace("spell-name", get("spell-name"))
                text = text.replace("spell-description", get("spell-description"))
                text = text.replace("spell-level", get("spell-level"))
                text = text.replace("spell-school", get("spell-school"))
                text = text.replace("has-spell-traits", get("has-spell-traits"))
                text = text.replace("spell-traits", get("spell-traits"))
                text = text.replace("spell-source", get("spell-source"))
                text = text.replace("spell-casting-time", get("spell-casting-time"))
                text = text.replace("spell-components", get("spell-components"))
                text = text.replace("spell-range", get("spell-range"))

                text = text.replace("spell-tag0", get("spell-tag0"))
                text = text.replace("spell-tag1", get("spell-tag1"))
                text = text.replace("spell-tag2", get("spell-tag2"))
                text = text.replace("spell-value0", get("spell-value0"))
                text = text.replace("spell-value1", get("spell-value1"))
                text = text.replace("spell-value2", get("spell-value2"))

                text = text.replace("has-heightened0", get("has-heightened0"))
                text = text.replace("has-heightened1", get("has-heightened1"))
                text = text.replace("has-heightened2", get("has-heightened2"))
                text = text.replace("has-heightened3", get("has-heightened3"))
                text = text.replace("spell-heightened-level0", get("spell-heightened-level0"))
                text = text.replace("spell-heightened-level1", get("spell-heightened-level1"))
                text = text.replace("spell-heightened-level2", get("spell-heightened-level2"))
                text = text.replace("spell-heightened-level3", get("spell-heightened-level3"))
                text = text.replace("spell-heightened-description0", get("spell-heightened-description0"))
                text = text.replace("spell-heightened-description1", get("spell-heightened-description1"))
                text = text.replace("spell-heightened-description2", get("spell-heightened-description2"))
                text = text.replace("spell-heightened-description3", get("spell-heightened-description3"))

                text = text.replace("has-spell-action", get("has-spell-action"))
                text = text.replace("has-spell-action-trigger", get("has-spell-action-trigger"))
                text = text.replace("spell-action-title", get("spell-action-title"))
                text = text.replace("spell-action-time", get("spell-action-time"))
                text = text.replace("spell-action-trigger", get("spell-action-trigger"))
                text = text.replace("spell-action-effect", get("spell-action-effect"))

                text = text.replace("has-saving-cs", get("has-saving-cs"))
                text = text.replace("has-saving-s", get("has-saving-s"))
                text = text.replace("has-saving-f", get("has-saving-f"))
                text = text.replace("has-saving-cf", get("has-saving-cf"))
                text = text.replace("spell-saving-critical-success", get("spell-saving-critical-success"))
                text = text.replace("spell-saving-success", get("spell-saving-success"))
                text = text.replace("spell-saving-failure", get("spell-saving-failure"))
                text = text.replace("spell-saving-critical-failure", get("spell-saving-critical-failure"))


                outputF = open("output/spell-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/spell-" + title + ".tex -output-directory=output -job-name=spell-" + title)


process_spell_cards()

files = os.listdir("output")
files = [f for f in files if ".pdf" not in f]
for f in files:
    os.remove("output/" + f)