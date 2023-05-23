import json
import os
import re
import subprocess

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

            outputF = open("output/" + title + ".tex", 'w')
            outputF.write(text)
            outputF.close()

            subprocess.call("pdflatex output/" + title + ".tex -output-directory=output -job-name=" + title)

files = os.listdir("output")
files = [f for f in files if ".pdf" not in f]
for f in files:
    os.remove("output/" + f)