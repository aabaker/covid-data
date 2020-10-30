#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot
from matplotlib import dates
import csv
import sys

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
    ax.plot_date(dates[238:-2], places[location].rate[238:-2], fmt='-', label=places[location].name)

places = {}
with open('places-7day.csv') as csvfile:
  reader = csv.reader(csvfile)
  head = next(reader)
  for row in reader:
    places[row[0]] = Place(row)

dates = matplotlib.dates.datestr2num(head[4:])

if len(sys.argv) != 2:
    print("Syntax: " + sys.argv[0] + " places_file")
    sys.exit(1)

fig, ax = matplotlib.pyplot.subplots()
with open(sys.argv[1]) as plotplaces:
    placeList = plotplaces.readlines()
    for code in placeList:
        plotLocation(ax, dates, places, code.strip())

ax.legend()
ax.grid(True)
fig.autofmt_xdate()
matplotlib.pyplot.show()
