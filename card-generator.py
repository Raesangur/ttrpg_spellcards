import json
import os
import re
import subprocess
import abc

class CardGenerator(metaclass = abc.ABCMeta):
    def __init__(self, name):
        self.name = name

    def process(self):
        open_template()
        open_cards()

        # Iterate over all cards in the .json file
        for card in self.cardsDict["cards"]:
            title = get_title(card)
            cardText = self.templateText.copy()

            # Skip the card if it already exists
            if card_already_exists(title):
                continue

            insert_newlines(card)

            # These functions are virtual and defined by child classes
            card_specific_processing(card, title)
            card_specific_attribute_replacement(card, cardText)

            # Sent the output to a final .tex file and run pdflatex on it
            write_output_file(title, cardText)


    def open_template(self):
        with open("template-spell.tex", 'r') as templateFile: 
            self.templateText = templateFile.read()

    def open_cards(self):
        with open("cards-spell.json", 'r') as cards:
            cardsDict = json.load(cards)

    def get_title(self, card):
        return card[self.name + "-title"].replace(' ', '_').lower()

    def card_already_exists(self, title):
        if self.name + "-" + title + ".pdf" in os.listdir("output"):
            print(self.name + " - " + title + " already exists, skipping...")
            return True
        return False

    def write_output_file(self, title, cardText):
        with open("output/" + self.name + "-" + title + ".tex", 'w') as outputFile:
            outputFile.write(cardText)

        subprocess.call("pdflatex output/" + self.name + "spell-" + title + ".tex -output-directory=output -job-name=" + self.name + "-" + title)

    def insert_newlines(card):
        for k in card.keys():
            card[k] = card[k].replace("\n", "\\\\\n\\vspace{2.5mm}\\\\\n")

    def compute_attribute_flags(card, attributeFlag, attributeName, N = None, delimiter = '%', noDelimiter = ''):
        def m_compute_attribute_flags(card, attributeFlag, attributeName, N, delimiter, noDelimiter):
            if attributeName in card:
                card[attributeFlag] = noDelimiter
            else:
                card[attributeFlag] = delimiter

        if N == None:
            m_compute_attribute_flags(card, attributeFlag, attributeName, N, delimiter, noDelimiter)

        else:
            for n in range(0, N):
                # Append the number to the attribute name
                attribName = attributeName + n
                attribFlag = attributeFlag + n

                m_compute_attribute_flags(card, attribFlag, attribName, N, delimiter, noDelimiter)

    def ajust_spacing(self, title):
        spaces = card[self.name + "-title"].count(' ')
        
        spacing  = "10mm" if len(title) < (20 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"
        spacing2 =  str(3 if len(title) < (20 + spaces) else 9 if len(title) < (32 + spaces) else 13) + "mm"

        return spacing, spacing2

    def configure_attribute(self, cardText, attributeName, attributeValue = None):
        if attributeValue == None:
            attributeValue = attributeName
        return cardText.replace(attributeName, card.get(attributeValue, ""))

    @abc.abstractmethod
    def card_specific_processing(self, card, title):
        pass

    @abc.abstractmethod
    def card_specific_attribute_replacement(self, card, cardText):
        pass


class SpellCardGenerator(CardGenerator):
    @abc.abstractmethod
    def card_specific_processing(self, card, title):
        pass

    @abc.abstractmethod
    def card_specific_attribute_replacement(self, card, cardText):

        attributeList = [ "spell-title", "spell-description", "spell-level", "spell-school",
                          "has-spell-traits", "spell-traits", "spell-source",
                          "spell-casting-time", "spell-components", "spell-range",
                          "spell-tag0", "spell-tag1", "spell-tag2",
                          "spell-value0", "spell-value1", "spell-value2",
                          "has-heightened0", "has-heightened1", "has-heightened2",
                          "has-heightened3", "has-heightened4", "has-heightened5",
                          "has-heightened6", "has-heightened7", "has-heightened8",
                          "has-heightened9", "spell-heightened-level0", "spell-heightened-level1",
                          "spell-heightened-level2", "spell-heightened-level3",
                          "spell-heightened-level4", "spell-heightened-level5",
                          "spell-heightened-level6", "spell-heightened-level7",
                          "spell-heightened-level8", "spell-heightened-description0",
                          "spell-heightened-description1", "spell-heightened-description2",
                          "spell-heightened-description3", "spell-heightened-description4",
                          "spell-heightened-description5", "spell-heightened-description6",
                          "spell-heightened-description7", "spell-heightened-description8",
                          "has-spell-action", "has-spell-action-trigger",
                          "spell-action-title", "spell-action-time", "spell-action-trigger",
                          "spell-action-effect", "has-saving-cs", "has-saving-s", "has-saving-f",
                          "has-saving-cf", "spell-saving-critical-success", "spell-saving-success",
                          "spell-saving-failure", "spell-saving-critical-failure"]

        for attrib in attributeList:
            cardText = configure_attribute(cardText, attrib)



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

    if "spell-heightened-level4" in card:
        card["has-heightened4"] = ""
    else:
        card["has-heightened4"] = "%"

    if "spell-heightened-level5" in card:
        card["has-heightened5"] = ""
    else:
        card["has-heightened5"] = "%"

    if "spell-heightened-level6" in card:
        card["has-heightened6"] = ""
    else:
        card["has-heightened6"] = "%"

    if "spell-heightened-level7" in card:
        card["has-heightened7"] = ""
    else:
        card["has-heightened7"] = "%"

    if "spell-heightened-level8" in card:
        card["has-heightened8"] = ""
    else:
        card["has-heightened8"] = "%"

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

def check_item_components(card):
    # Check Level
    if "item-level" in card:
        card["has-level"] = ""
    else:
        card["has-level"] = "%"

    # Check Rarity
    if "item-rarity" in card:
        card["has-rarity"] = ""
    else:
        card["has-rarity"] = "%"

    # Check Traits
    if "item-trait0" in card:
        card["has-trait0"] = ""
    else:
        card["has-trait0"] = "%"

    if "item-trait1" in card:
        card["has-trait1"] = ""
    else:
        card["has-trait1"] = "%"

    if "item-trait2" in card:
        card["has-trait2"] = ""
    else:
        card["has-trait2"] = "%"

    if "item-trait3" in card:
        card["has-trait3"] = ""
    else:
        card["has-trait3"] = "%"

    # Check runes
    card["has-runes"] = "%"
    if "item-rune0" in card:
        card["has-rune0"] = ""
        card["has-runes"] = ""
    else:
        card["has-rune0"] = "%"

    if "item-rune1" in card:
        card["has-rune1"] = ""
        card["has-runes"] = ""
    else:
        card["has-rune1"] = "%"

    if "item-rune2" in card:
        card["has-rune2"] = ""
        card["has-runes"] = ""
    else:
        card["has-rune2"] = "%"


    # Check actions
    if "item-action0-title" in card:
        card["has-item-action0"] = ""
    else:
        card["has-item-action0"] = "%"
    if "item-action0-trigger" in card:
        card["has-trigger-item-action0"] = ""
    else:
        card["has-trigger-item-action0"] = "%"

    if "item-action1-title" in card:
        card["has-item-action1"] = ""
    else:
        card["has-item-action1"] = "%"
    if "item-action1-trigger" in card:
        card["has-trigger-item-action1"] = ""
    else:
        card["has-trigger-item-action1"] = "%"

    if "item-damage" in card:
        card["is-weapon"] = ""
    else:
        card["is-weapon"] = "%"

    if "item-critical-specialization" in card:
        card["has-critical-specialization"] = ""
    else:
        card["has-critical-specialization"] = "%"


def check_traits_length(card, threshold = 20):
    length = 0
    
    if card["has-trait0"] == "":
        length = length + len(card["item-trait0"])

    if card["has-trait1"] == "":
        length = length + len(card["item-trait1"])

    if card["has-trait2"] == "":
        length = length + len(card["item-trait2"])

    if card["has-trait3"] == "":
        length = length + len(card["item-trait3"])

    if length > threshold:
        card["has-short-traits"] = "%"
        card["has-long-traits"] = ""
    else:
        card["has-short-traits"] = ""
        card["has-long-traits"] = "%"


def check_item_rarity(card):
    card["rarity-color"] = "common-color"

    if card["has-rarity"] == "":
        if card["item-rarity"].lower() == "uncommon":
            card["rarity-color"] = "uncommon-color"
        if card["item-rarity"].lower() == "rare":
            card["rarity-color"] = "rare-color"
        if card["item-rarity"].lower() == "unique":
            card["rarity-color"] = "unique-color"

def process_item_runes(card):
    if "item-rune0" in card:
        ch = card["item-rune0"][0].lower()
        print(ch)
        card["item-rune0-image"] = ch

    if "item-rune1" in card:
        ch = card["item-rune1"][0].lower()
        print(ch)
        card["item-rune1-image"] = ch

    if "item-rune2" in card:
        ch = card["item-rune2"][0].lower()
        print(ch)
        card["item-rune2-image"] = ch

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

def adjust_spell_fontsize(card):
    equivalentCharacters = len(card["spell-description"]) + 20 * card["spell-description"].count('\n')

    for n in range(0, 8):
        if card["has-heightened" + str(n)] != "%":
            equivalentCharacters += len(card["spell-heightened-description" + str(n)]) + 20 + 10

    if card["has-spell-action"] != "%":
        equivalentCharacters += len(card["spell-action-effect"]) + 40 + 20

    if card["has-saving-cs"] != "%":
        equivalentCharacters += len(card["spell-saving-critical-success"]) + 20 + 20
    if card["has-saving-s"] != "%":
        equivalentCharacters += len(card["spell-saving-success"]) + 20 + 20
    if card["has-saving-f"] != "%":
        equivalentCharacters += len(card["spell-saving-failure"]) + 20 + 20
    if card["has-saving-cf"] != "%":
        equivalentCharacters += len(card["spell-saving-critical-failure"]) + 20 + 20

    if equivalentCharacters <= 800:
        card["spell-font-size"] = "9"
    elif equivalentCharacters <= 1350:
        card["spell-font-size"] = "8"
    else:
        card["spell-font-size"] = "7"

def insert_newlines(card):
 for k in card.keys():
     card[k] = card[k].replace("\n", "\\\\\n\\vspace{2.5mm}\\\\\n")

def process_hero_cards():
    with open("template-hero.tex", 'r') as inputF: 
        template = inputF.read()

        with open("cards-hero.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                spaces = card["hero-title"].count(' ')
                title = card["hero-title"].replace(' ', '_')

                if "hero-" + title + ".pdf" in os.listdir("output"):
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
                text = text.replace("hero-spacing-secondary", spacing2)
                text = text.replace("hero-spacing",  spacing)

                outputF = open("output/hero-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/hero-" + title + ".tex -output-directory=output -job-name=" + title)

def process_alchemy_cards():
    with open("template-alchemy.tex", 'r') as inputF: 
        template = inputF.read()

        with open("cards-alchemy.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                title = card["alchemy-title"].replace(' ', '_').replace('(', '').replace(')', '')

                if "alchemy-" + title + ".pdf" in os.listdir("output"):
                    print(title + " already exists, skipping...")
                    continue

                spaces = card["alchemy-title"].count(' ')
                spacing  = "10mm" if len(title) < (17 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"
                spacing2 =  str(3 if len(title) < (13 + spaces) else 9 if len(title) < (29 + spaces) else 13) + "mm"

                text = template.replace("alchemy-title", card["alchemy-title"])
                text = text.replace("alchemy-type", card["alchemy-type"])
                text = text.replace("alchemy-activation", card["alchemy-activation"])
                text = text.replace("alchemy-bulk", card["alchemy-bulk"])
                text = text.replace("alchemy-usage", card["alchemy-usage"])
                text = text.replace("alchemy-spacing-secondary", spacing2)
                text = text.replace("alchemy-spacing", spacing)
                text = text.replace("alchemy-description", card["alchemy-description"])

                outputF = open("output/alchemy-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/alchemy-" + title + ".tex -output-directory=output -job-name=alchemy-" + title)

def process_item_cards():
    with open("template-item.tex", 'r') as inputF: 
        template = inputF.read()

        with open("cards-item.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                def get(string):
                    return card.get(string, "")

                title = card["item-title"].replace(' ', '_').replace('(', '').replace(')', '')

                if "item-" + title + ".pdf" in os.listdir("output"):
                    print(title + " already exists, skipping...")
                    continue

                check_item_components(card)
                insert_newlines(card)
                check_traits_length(card)
                check_item_rarity(card)
                process_item_runes(card)

                spaces = sum(card["item-title"].count(x) for x in (' ', '+', '\''))
                spacing  = "10mm" if len(title) < (20 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"
                spacing2 =  str(3 if len(title) < (20 + spaces) else 9 if len(title) < (32 + spaces) else 13) + "mm"

                text = template.replace("item-title", get("item-title"))
                text = text.replace("item-type", get("item-type"))
                text = text.replace("item-level", get("item-level"))
                text = text.replace("item-rarity", get("item-rarity"))
                text = text.replace("item-spacing-secondary", spacing2)
                text = text.replace("item-spacing", spacing)
                text = text.replace("item-description", get("item-description"))

                text = text.replace("has-level", get("has-level"))
                text = text.replace("has-rarity", get("has-rarity"))
                text = text.replace("rarity-color", get("rarity-color"))
                text = text.replace("has-trait0", get("has-trait0"))
                text = text.replace("has-trait1", get("has-trait1"))
                text = text.replace("has-trait2", get("has-trait2"))
                text = text.replace("has-trait3", get("has-trait3"))
                text = text.replace("item-trait0", get("item-trait0"))
                text = text.replace("item-trait1", get("item-trait1"))
                text = text.replace("item-trait2", get("item-trait2"))
                text = text.replace("item-trait3", get("item-trait3"))
                text = text.replace("has-short-traits", get("has-short-traits"))
                text = text.replace("has-long-traits", get("has-long-traits"))
                text = text.replace("is-weapon", get("is-weapon"))
                text = text.replace("item-damage", get("item-damage"))
                text = text.replace("item-wield", get("item-wield"))

                text = text.replace("has-runes", get("has-runes"))
                text = text.replace("has-rune0", get("has-rune0"))
                text = text.replace("has-rune1", get("has-rune1"))
                text = text.replace("has-rune2", get("has-rune2"))
                text = text.replace("item-rune0-image", get("item-rune0-image"))
                text = text.replace("item-rune1-image", get("item-rune1-image"))
                text = text.replace("item-rune2-image", get("item-rune2-image"))
                text = text.replace("item-rune0-description", get("item-rune0-description"))
                text = text.replace("item-rune1-description", get("item-rune1-description"))
                text = text.replace("item-rune2-description", get("item-rune2-description"))
                text = text.replace("item-rune0", get("item-rune0"))
                text = text.replace("item-rune1", get("item-rune1"))
                text = text.replace("item-rune2", get("item-rune2"))

                text = text.replace("has-critical-specialization", get("has-critical-specialization"))
                text = text.replace("item-critical-specialization", get("item-critical-specialization"))

                text = text.replace("has-item-action0", get("has-item-action0"))
                text = text.replace("has-item-action1", get("has-item-action1"))
                text = text.replace("has-trigger-item-action0", get("has-trigger-item-action0"))
                text = text.replace("has-trigger-item-action1", get("has-trigger-item-action1"))
                text = text.replace("item-action0-title", get("item-action0-title"))
                text = text.replace("item-action1-title", get("item-action1-title"))
                text = text.replace("item-action0-traits", get("item-action0-traits"))
                text = text.replace("item-action1-traits", get("item-action1-traits"))
                text = text.replace("item-action0-time", get("item-action0-time"))
                text = text.replace("item-action1-time", get("item-action1-time"))
                text = text.replace("item-action0-description", get("item-action0-description"))
                text = text.replace("item-action1-description", get("item-action1-description"))
                text = text.replace("item-action0-trigger", get("item-action0-trigger"))
                text = text.replace("item-action1-trigger", get("item-action1-trigger"))

                outputF = open("output/item-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/item-" + title + ".tex -output-directory=output -job-name=item-" + title)

def process_spell_cards():
    with open("template-spell.tex", 'r') as inputF: 
        template = inputF.read()

        with open("cards-spell.json", 'r') as cards:
            cards_dict = json.load(cards)

            for card in cards_dict["cards"]:
                def get(string):
                    return card.get(string, "")

                spaces = card["spell-title"].count(' ')
                title = card["spell-title"].replace(' ', '_').lower()

                if "spell-" + title + ".pdf" in os.listdir("output"):
                    print(title + " already exists, skipping...")
                    continue

                #spacing  = "10mm" if len(title) < (17 + spaces) else "16mm" if len(title) < (32 + spaces) else "20mm"
                
                check_spell_components(card)
                make_spell_tags(card)
                adjust_spell_fontsize(card)
                insert_newlines(card)


                text = template.replace("spell-title", get("spell-title"))
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
                text = text.replace("has-heightened4", get("has-heightened4"))
                text = text.replace("has-heightened5", get("has-heightened5"))
                text = text.replace("has-heightened6", get("has-heightened6"))
                text = text.replace("has-heightened7", get("has-heightened7"))
                text = text.replace("has-heightened8", get("has-heightened8"))
                text = text.replace("spell-heightened-level0", get("spell-heightened-level0"))
                text = text.replace("spell-heightened-level1", get("spell-heightened-level1"))
                text = text.replace("spell-heightened-level2", get("spell-heightened-level2"))
                text = text.replace("spell-heightened-level3", get("spell-heightened-level3"))
                text = text.replace("spell-heightened-level4", get("spell-heightened-level4"))
                text = text.replace("spell-heightened-level5", get("spell-heightened-level5"))
                text = text.replace("spell-heightened-level6", get("spell-heightened-level6"))
                text = text.replace("spell-heightened-level7", get("spell-heightened-level7"))
                text = text.replace("spell-heightened-level8", get("spell-heightened-level8"))
                text = text.replace("spell-heightened-description0", get("spell-heightened-description0"))
                text = text.replace("spell-heightened-description1", get("spell-heightened-description1"))
                text = text.replace("spell-heightened-description2", get("spell-heightened-description2"))
                text = text.replace("spell-heightened-description3", get("spell-heightened-description3"))
                text = text.replace("spell-heightened-description4", get("spell-heightened-description4"))
                text = text.replace("spell-heightened-description5", get("spell-heightened-description5"))
                text = text.replace("spell-heightened-description6", get("spell-heightened-description6"))
                text = text.replace("spell-heightened-description7", get("spell-heightened-description7"))
                text = text.replace("spell-heightened-description8", get("spell-heightened-description8"))

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

                text = text.replace("spell-font-size", get("spell-font-size"))


                outputF = open("output/spell-" + title + ".tex", 'w')
                outputF.write(text)
                outputF.close()

                subprocess.call("pdflatex output/spell-" + title + ".tex -output-directory=output -job-name=spell-" + title)


#process_hero_cards()
process_spell_cards()
process_alchemy_cards()
process_item_cards()

files = os.listdir("output")
files = [f for f in files if ".pdf" not in f]
for f in files:
    os.remove("output/" + f)
