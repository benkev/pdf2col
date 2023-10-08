help_txt = '''

sber2col_PyPDF2.py

Convert a long and narrow pdf file of Sber (Sberbank) receipt into
a 2-column Letter-page pdf file. Conversion is based on the 

Unfortunately, 

'''

import copy
import PyPDF2
import sys

# Source and output file names from command line arguments
f_src = sys.argv[1]
f_out = sys.argv[2]

# Output PDF dimensions in points
opdf_w = 306  # Width
opdf_h = 812  # Height

# Create a PdfReader object
rd = PyPDF2.PdfReader(f_src)

# Get the first page from the source PDF
pg = rd.pages[0]

# Create a PdfWriter object
wr = PyPDF2.PdfWriter()

# Create copies of the page to crop different areas
top_part = copy.copy(pg)
bottom_part = copy.copy(pg)

# Crop the top part
top_part.mediabox.lower_left = (0, opdf_h)
top_part.mediabox.upper_right = (opdf_w, pg.mediabox[3])

# Crop the bottom part
bottom_part.mediabox.lower_left = (0, 0)
bottom_part.mediabox.upper_right = (opdf_w, opdf_h)

# Create a new blank page with the dimensions for the two-column format
new_page = wr.add_blank_page(width=opdf_w * 2, height=opdf_h)

# Merge the top part of the source PDF to the left side of the new page
new_page.merge_page(top_part)
#new_page.merge_page(bottom_part)

# Merge the bottom part of the source PDF to the right side of the new page
new_page.mergeTranslatedPage(bottom_part, float(opdf_w), 0.)
#new_page.mergeTranslatedPage(top_part, float(opdf_w), 0.)

# Add the new two-column page to the writer object
wr.addPage(new_page)

# Write the new two-column PDF to a file
with open(f_out, 'wb') as f:
    wr.write(f)

print(f"Converted {f_src} to two-column format in {f_out}")
