# import module
from pdf2image import convert_from_path
import cv2
import numpy
import tkinter as tk
import tkinter.filedialog as fd

# Open file dialog and get 1 to n file paths
root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent = root, title = "pdf files to load")

for filename in filez:
      # Get filename, ignoring extension
      filename = filename.split(".", 1)[0]

      # Store Pdf with convert_from_path function
      images = convert_from_path(filename + ".pdf")
      for i in range(len(images)):
          # Convert PIL image to cv2 image
          img = images[i].convert('RGB')
          img = numpy.array(img)[:, :, ::-1].copy()

          # Scale image to 900 x 1500
          img = cv2.resize(img, (900, 1500), interpolation = cv2.INTER_AREA)

          # Save new image
          cv2.imwrite(filename + ".png", img)