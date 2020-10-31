#!/usr/bin/env python3

# Copyright 2020 Adam Baker
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this
#    list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import configparser
import csv
import datetime
import matplotlib
from matplotlib import pyplot
from matplotlib import dates
import os
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

def plotLocation(ax, dates, places, location, offset):
    ax.plot_date(dates[offset:], places[location].rate[offset:], fmt='-', label=places[location].name)

if len(sys.argv) != 2:
    print("Syntax: " + sys.argv[0] + " config_file")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(sys.argv[1])

places = {}
with open(os.path.join(config['DEFAULT']['DataDir'],'places-7day.csv')) as csvfile:
  reader = csv.reader(csvfile)
  # skip header row
  head = next(reader)
  for row in reader:
    places[row[0]] = Place(row)

dataStart = datetime.datetime.strptime(head[4], '%Y-%m-%d')
graphStart = datetime.datetime.strptime(config['DEFAULT']['GraphStart'], '%Y-%m-%d')
offset = graphStart - dataStart

# First 4 columns are header info
dates = matplotlib.dates.datestr2num(head[4:])

fig, ax = matplotlib.pyplot.subplots()
for code in config['DEFAULT']['Places'].splitlines():
    if code != '':
        plotLocation(ax, dates, places, code, offset.days)

ax.legend()
ax.grid(True)
fig.autofmt_xdate()
matplotlib.pyplot.show()
