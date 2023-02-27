from pdf2image import convert_from_path
import cv2
import numpy as np
import sys
import tkinter as tk
import tkinter.filedialog as fd

filez = []
if len(sys.argv) == 1:
    # Open file dialog and get 1 to n file paths
    root = tk.Tk()
    root.withdraw()
    filez = fd.askopenfilenames(parent = root, title = "Cards to load (up to 4)", filetypes=[("Portable Document Format", "*.pdf")])

    if (len(filez) > 4) or (len(filez) == 0):
        print("Max 4 cards at a time")
        exit()
else:
    cardBacks = {
    "abjuration"    : "./backs/back_abjuration.png",
    "conjuration"   : "./backs/back_conjuration.png",
    "divination"    : "./backs/back_divination.png",
    "enchantment"   : "./backs/back_enchantment.png",
    "evocation"     : "./backs/back_evocation.png",
    "illusion"      : "./backs/back_illusion.png",
    "necromancy"    : "./backs/back_necromancy.png",
    "transmutation" : "./backs/back_transmutation.png",

    "abj"     : "./backs/back_abjuration.png",
    "abjur"   : "./backs/back_abjuration.png",
    "con"     : "./backs/back_conjuration.png",
    "conjur"  : "./backs/back_conjuration.png",
    "div"     : "./backs/back_divination.png",
    "divi"    : "./backs/back_divination.png",
    "divin"   : "./backs/back_divination.png",
    "ench"    : "./backs/back_enchantment.png",
    "enchant" : "./backs/back_enchantment.png",
    "evo"     : "./backs/back_evocation.png",
    "evoca"   : "./backs/back_evocation.png",
    "illu"    : "./backs/back_illusion.png",
    "nec"     : "./backs/back_necromancy.png",
    "necro"   : "./backs/back_necromancy.png",
    "trans"   : "./backs/back_transmutation.png",
    }
    for arg in sys.argv[1:]:
        filez.append(cardBacks[arg])

#
cardWidth   = 900
cardHeight  = 1500
paperWidth  = 2550
paperHeight = 3300
firstCardX  = 250
firstCardY  = 100

# Create blank image of the right size
blankImage = np.ones((paperHeight, paperWidth, 3), dtype=np.uint8)
blankImage.fill(255)


# Add cards to the image
for i in range(len(filez)):
    # Read image and convert PIL image to cv2 image if PDF
    filename = filez[i]
    fileExtension = "." + filez[i].split(".")[-1]
    img = ""
    if fileExtension == ".png":
        img = cv2.imread(filename)
    elif fileExtension == ".pdf":
        img = convert_from_path(filename)[0].convert('RGB')
        img = np.array(img)[:, :, ::-1].copy()
    else:
        img = "error - unsupported file extension"

    # Scale image to 900 x 1500
    img = cv2.resize(img, (cardWidth, cardHeight), interpolation = cv2.INTER_AREA)

    # Calculate offsets
    x = i %  2
    y = i // 2
    xOff = firstCardX * (x + 1) + cardWidth  * x
    yOff = firstCardY * (y + 1) + cardHeight * y
    blankImage[yOff:yOff + img.shape[0], xOff:xOff + img.shape[1]] = img

# Add cutting guides
lineThickness = 1
lineColor = (0, 0, 0)
for i in [0, 1]:
    yOff1 = firstCardY * (i + 1) + cardHeight *  i      + 1
    yOff2 = firstCardY * (i + 1) + cardHeight * (i + 1) - 1
    xOff1 = firstCardX * (i + 1) + cardWidth  *  i      + 1
    xOff2 = firstCardX * (i + 1) + cardWidth  * (i + 1) - 1
    cv2.line(blankImage, (0, yOff1), (paperWidth, yOff1),  lineColor, thickness=lineThickness)
    cv2.line(blankImage, (0, yOff2), (paperWidth, yOff2),  lineColor, thickness=lineThickness)
    cv2.line(blankImage, (xOff1, 0), (xOff1, paperHeight), lineColor, thickness=lineThickness)
    cv2.line(blankImage, (xOff2, 0), (xOff2, paperHeight), lineColor, thickness=lineThickness)

# Save image
cv2.imwrite("newcards.png", blankImage)
