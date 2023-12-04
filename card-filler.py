from pdf2image import convert_from_path
from PIL       import Image
from PyPDF2    import PdfReader
import cv2
import math
import numpy as np
import sys
import tkinter as tk
import tkinter.filedialog as fd


def create_images(files, back_xOffset = 0, back_yOffset = 0):
    # Create blank image of the right size
    blankImage = np.ones((paperHeight, paperWidth, 3), dtype=np.uint8)
    backImage  = np.ones((paperHeight, paperWidth, 3), dtype=np.uint8)
    blankImage.fill(255)
    backImage.fill(255)

    # Add cards to the image
    for i in range(len(files)):
        # Extract image from PDF, convert to cv2 image and scale image
        filename = files[i]
        img = convert_from_path(filename, dpi=450)[0].convert('RGB')
        img = np.array(img)[:, :, ::-1].copy()
        img = cv2.resize(img, (cardWidth, cardHeight), interpolation = cv2.INTER_AREA)

        # Extract school of magic picture
        text        = PdfReader(filename).pages[0].extract_text().lower()
        school      = sorted([word for word in schoolList if word in text])
        print(school)
        schoolBack  = cardBacksPath + school[0] + ".png" #cardBacks[school[0].lower()]
        schoolFront = cardFrontsPath + school[0] + ".png" #cardFronts[school[0].lower()]
        back        = cv2.imread(schoolBack)
        front       = cv2.imread(schoolFront, cv2.IMREAD_UNCHANGED)

        alpha = np.ones(img.shape, dtype=np.uint8)
        alpha[:, :, 0] = front[:, :, 3]
        alpha[:, :, 1] = front[:, :, 3]
        alpha[:, :, 2] = front[:, :, 3]

        alpha = alpha.astype(float)/255
        front = front.astype(float)
        img   = img.astype(float)

        front = cv2.multiply(alpha, front[:, :, :3])
        img   = cv2.multiply(1.0 - alpha, img)

        # Calculate offsets
        y  = i // 2
        x  = i %  2
        xb = (i + 1) % 2

        xOff  = firstCardX * (x + 1)  + cardWidth  * x
        xOffb = firstCardX * (xb + 1) + cardWidth  * xb
        yOff  = firstCardY * (y + 1)  + cardHeight * y
        blankImage[yOff:yOff + img.shape[0],  xOff :xOff  + img.shape[1]]  = cv2.add(img, front)
        backImage [yOff + back_yOffset : yOff + back_yOffset + back.shape[0], xOffb + back_xOffset : xOffb + back_xOffset + back.shape[1]] = back

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
        cv2.line(backImage,  (0, yOff1 + back_yOffset), (paperWidth, yOff1 + back_yOffset),  lineColor, thickness=lineThickness)
        cv2.line(backImage,  (0, yOff2 + back_yOffset), (paperWidth, yOff2 + back_yOffset),  lineColor, thickness=lineThickness)
        cv2.line(backImage,  (xOff1 + back_xOffset, 0), (xOff1 + back_xOffset, paperHeight), lineColor, thickness=lineThickness)
        cv2.line(backImage,  (xOff2 + back_xOffset, 0), (xOff2 + back_xOffset, paperHeight), lineColor, thickness=lineThickness)

    return blankImage, backImage

# Open file dialog and get 1 to n file paths
root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent = root, title = "Cards to load", filetypes=[("Portable Document Format", "*.pdf")])

cardBacksPath = "./backs/back_"
cardFrontsPath = "./backs/front_"
schoolList = ["abjuration", "conjuration", "divination", "enchantment", "evocation", "illusion", "necromancy", "transmutation",
              "hero", "barbarian", "loky", "alchemy", "metamagic", "adelaide", "loot", "christmas"]

#
cardWidth   = 900
cardHeight  = 1500
paperWidth  = 2550
paperHeight = 3300
firstCardX  = 250
firstCardY  = 100
paperHeightmm = 279.4
paperWidthmm  = 215.9

yOffset = int(2 * paperHeight // paperHeightmm)       # There is a 2mm offset between the front and the back, probably caused by the printer itself

images = []
for i in range(math.ceil(len(filez) / 4)):
    frontImage, backImage = create_images(filez[i * 4: i * 4 + 4], back_yOffset = yOffset)
    images.append(Image.fromarray(frontImage[...,::-1]))
    images.append(Image.fromarray(backImage[...,::-1]))

images[0].save("output.pdf", "PDF", resolutionm=450.0, save_all=True, append_images=images[1:])

