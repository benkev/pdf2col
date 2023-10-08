help_txt = '''

sber2col.py

Convert a long and narrow pdf file of Sber (Sberbank) receipt into
a 2-column Letter-page pdf file.
The name of generated file is the same as input with "_2col" appended
before the ".pdf" extension.

Example:
$ python sber2col.py abc.pdf

Ouput file: abc_2col.pdf

10/07/2023, Leonid Benkevitch.
'''

import numpy as np
import sys, os
import subprocess

if len(sys.argv) < 2:
    print(help_txt)
    sys.exit()
    
f_in = sys.argv[1]

f_out = os.path.splitext(f_in)[0] + "_2col.pdf"

col_w = 324       # Output pdf file page width, 4.5 inch = 324/72
col_h = 812       # Output pdf file page height, 11.28 inch = 812/72       

cmd1 = "pdfinfo " + f_in + " | grep 'Page size' | awk '{print $3, $5}'"

#
# subprocess.run() is used to run the command.
#   shell=True means the command is executed through the shell (note that this
#              can be a security hazard if combined with untrusted input).
#   stdout=subprocess.PIPE and stderr=subprocess.PIPE mean that the stdout
#              and stderr outputs of the command are captured.
#   text=True means that the output and errors are captured as strings;
#             if you omit this, they will be captured as bytes.
#

cpr = subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True)

if cpr.stderr != '':
    print(cmd1 + "\n" + cpr.stderr)

#
# After running the command, cpr is a "completed process".
# cpr.stdout contains the stdout output as a string, and
# cpr.stderr contains the stderr output as a string.
#

# print(cpr.stdout)

sz = cpr.stdout
sz = np.array(sz.split(), dtype=int)

iw = sz[0]       # Input pdf file page width
ih = sz[1]       # Input pdf file page height

n_chn = ih // col_h + 1  # Number of chunks
l_chn = ih % col_h       # Last chunk size, pt
if l_chn == 0:
    l_chn = col_h
    n_chn = n_chn - 1
    
sl_chn = " " + str(l_chn)
scol_w = " " + str(col_w)
scol_h = " " + str(col_h)
sih = " " + str(ih)

top_box = "0" + sl_chn + scol_w + sih
bot_box = "0 0 " + scol_w + sl_chn

print("File \"%s\" \nPage size: %.2f x %.2f (points) or %.2f x %.2f (inches)" %
      (f_in, iw, ih, iw/72, ih/72))

print("Number of chunks: %d;  Last chunk size, pt: %d" % (n_chn, l_chn))

cmd2 = "gs -o __bot__.pdf -sDEVICE=pdfwrite " + \
          "-c '[/CropBox [" + bot_box + "] /PAGES pdfmark' -f " + f_in 

cmd3 = "gs -o __top__.pdf -sDEVICE=pdfwrite " + \
          "-c '[/CropBox [" + top_box + "] /PAGES pdfmark' -f " + f_in

# cmd2 = "gs -o __bot__.pdf -sDEVICE=pdfwrite " + \
#           "-c '[/CropBox [0 0 324 812] /PAGES pdfmark' -f " + f_in 

# cmd3 = "gs -o __top__.pdf -sDEVICE=pdfwrite " + \
#           "-c '[/CropBox [0 812 324 1624] /PAGES pdfmark' -f " + f_in

cmd4 = "pdfjam __top__.pdf __bot__.pdf --nup 2x1 --no-landscape -q " + \
                                      "--outfile " + f_out

cpr = subprocess.run(cmd2, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True)

if cpr.stderr != '':
    print(cmd2 + "\n" + cpr.stderr)
    sys.exit()

cpr = subprocess.run(cmd3, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True)

if cpr.stderr != '':
    print(cmd3 + "\n" + cpr.stderr)
    sys.exit()

cpr = subprocess.run(cmd4, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True)

if cpr.stderr != '':
    print(cmd4 + "\n" + cpr.stderr)
else:
    os.remove("__bot__.pdf")
    os.remove("__top__.pdf")



                                                 

                                                 
