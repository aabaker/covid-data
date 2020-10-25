#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot
from matplotlib import dates
import csv

class Place:
    def __init__(self, row):
        self.population = row[2]
        self.name = row[1]
        self.code = row[0]
        self.category = row[3]
        self.rate = []
        for x in row[4:]:
            self.rate.append(float(x))

def plotLocation(ax, dates, places, location):
    ax.plot_date(dates[160:], places[location].rate[160:], fmt='-', label=places[location].name)

places = {}
with open('places-7day.csv') as csvfile:
  reader = csv.reader(csvfile)
  head = next(reader)
  for row in reader:
    places[row[0]] = Place(row)

dates = matplotlib.dates.datestr2num(head[4:])

fig, ax = matplotlib.pyplot.subplots()
plotLocation(ax, dates, places, 'E06000018')
plotLocation(ax, dates, places, 'E07000091')
#ax.plot_date(dates, places['E06000018'].rate, fmt='-')
#ax.plot_date(dates, places['E07000091'].rate, fmt='-')
ax.legend()
ax.grid(True)
fig.autofmt_xdate()
matplotlib.pyplot.show()
