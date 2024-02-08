import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path
from fillpdf import fillpdfs

# Open file dialog and get 1 to n file paths
root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent = root, title = "Character sheets to load", filetypes=[("Portable Document Format", "*.pdf")])

for cs in filez:
    characterName = Path(cs).stem
    print(characterName)
    newName = cs.replace(".pdf", "-new.pdf")
    
    fillpdfs.get_form_fields(cs)
    fillpdfs.write_fillable_pdf(cs, newName, data_dict)
