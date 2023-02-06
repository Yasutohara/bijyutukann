import sys
import csv

from itertools import product
from reportlab.pdfgen import canvas
from reportlab.lib.colors import snow
from reportlab.lib.colors import black

basename = sys.argv[1]
with open(basename+'.csv') as inp_f:
  reader = csv.reader(inp_f)
  data = [row for row in reader]

sizes = data.pop(0)
rows = int(sizes[0])
cols = int(sizes[1])

ylist = list(range(50, 50*(rows+2), 50))
xlist = list(range(50, 50*(cols+2), 50))

c = canvas.Canvas(basename+'.pdf',bottomup=False)
c.setPageSize((xlist[-1]+50, ylist[-1]+50))

c.grid(xlist, ylist)
c.setStrokeColor(snow)

for y, x in product(range(rows), range(cols)):
  if 'x' in data[y][x]:
    c.rect(xlist[x], ylist[y], 50, 50, fill=True)
  elif '\\' in data[y][x]:
    c.rect(xlist[x], ylist[y], 50, 50, fill=True)
    former, latter = data[y][x].split('\\')
    c.line(xlist[x], ylist[y], xlist[x+1], ylist[y+1])
    c.setFontSize(24)
    c.setFillColor(snow)
    c.drawCentredString(xlist[x]+15, ylist[y]+47, former)
    c.drawCentredString(xlist[x]+35, ylist[y]+21, latter)
    c.setFillColor(black)
  else:
    c.setFontSize(40)
    c.drawCentredString(xlist[x]+25, ylist[y]+42, data[y][x])

c.showPage()
c.save()
