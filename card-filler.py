from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import cv2
import numpy as np
import sys
import tkinter as tk
import tkinter.filedialog as fd

# Open file dialog and get 1 to n file paths
root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent = root, title = "Cards to load (up to 4)", filetypes=[("Portable Document Format", "*.pdf")])

if (len(filez) > 4) or (len(filez) == 0):
    print("Max 4 cards at a time")
    exit()

cardBacks = {
"abjuration"    : "./backs/back_abjuration.png",
"conjuration"   : "./backs/back_conjuration.png",
"divination"    : "./backs/back_divination.png",
"enchantment"   : "./backs/back_enchantment.png",
"evocation"     : "./backs/back_evocation.png",
"illusion"      : "./backs/back_illusion.png",
"necromancy"    : "./backs/back_necromancy.png",
"transmutation" : "./backs/back_transmutation.png",
}

schoolList = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation", \
              "abjuration", "conjuration", "divination", "enchantment", "evocation", "illusion", "necromancy", "transmutation"]

#
cardWidth   = 900
cardHeight  = 1500
paperWidth  = 2550
paperHeight = 3300
firstCardX  = 250
firstCardY  = 100

# Create blank image of the right size
blankImage = np.ones((paperHeight, paperWidth, 3), dtype=np.uint8)
backImage  = np.ones((paperHeight, paperWidth, 3), dtype=np.uint8)
blankImage.fill(255)
backImage.fill(255)

# Add cards to the image
for i in range(len(filez)):
    # Extract image from PDF, convert to cv2 image and scale image
    filename = filez[i]
    img = convert_from_path(filename)[0].convert('RGB')
    img = np.array(img)[:, :, ::-1].copy()
    img = cv2.resize(img, (cardWidth, cardHeight), interpolation = cv2.INTER_AREA)

    # Extract school of magic picture
    text       = PdfReader(filename).pages[0].extract_text()
    school     = [word for word in schoolList if word in text]
    schoolBack = cardBacks[school[0].lower()]
    back       = cv2.imread(schoolBack)

    # Calculate offsets
    y  = i // 2
    x  = i %  2
    xb = (i + 1) % 2

    xOff  = firstCardX * (x + 1)  + cardWidth  * x
    xOffb = firstCardX * (xb + 1) + cardWidth  * xb
    yOff  = firstCardY * (y + 1)  + cardHeight * y
    blankImage[yOff:yOff + img.shape[0],  xOff :xOff  + img.shape[1]]  = img
    backImage [yOff:yOff + back.shape[0], xOffb:xOffb + back.shape[1]] = back

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
    cv2.line(backImage,  (0, yOff1), (paperWidth, yOff1),  lineColor, thickness=lineThickness)
    cv2.line(backImage,  (0, yOff2), (paperWidth, yOff2),  lineColor, thickness=lineThickness)
    cv2.line(backImage,  (xOff1, 0), (xOff1, paperHeight), lineColor, thickness=lineThickness)
    cv2.line(backImage,  (xOff2, 0), (xOff2, paperHeight), lineColor, thickness=lineThickness)

# Save image
cv2.imwrite("newcards.png",  blankImage)
cv2.imwrite("cardbacks.png", backImage)
