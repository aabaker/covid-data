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

import requests
import csv
import codecs
from contextlib import closing
import datetime

url = 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv'

class Place:
    def __init__(self, code, name, population):
        self.population = population
        self.name = name
        self.code = code
        self.cases = []
    def addCases(self, daynum, num):
        while (len(self.cases) <= daynum):
            self.cases.append(0)
        self.cases[daynum] = num
    def totalCases(self):
        return sum(self.cases)
    def rateOverInterval(self, end, days):
        return sum(self.cases[end - days:end]) / self.population * 100000
    def format(self, day):
        result = self.name
        result += ', This Week: '
        result += f'{self.rateOverInterval(day, 7):.2f}'
        result += ', Last Week: '
        result += f'{self.rateOverInterval(day - 7, 7):.2f}'
        result += ', Total: '
        result += f'{self.rateOverInterval(day, day):.2f}'
        result += ', Population: '
        result += f'{self.population:.0f}'
        return result

places = {}
with open('population.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) # skip header
    for row in reader:
        places[row[0]] = Place(row[0], row[1], float(row[2].replace(',','')))

jan1 = datetime.date(2020, 1, 1)
newest = jan1
with closing(requests.get(url, stream=True)) as r:
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
    next(reader) # skip header
    for row in reader:
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d').date()
        if row_date > newest:
            newest = row_date
        if row[1] in places:
            places[row[1]].addCases((row_date-jan1).days, int(row[4]))
        else:
            print('Unknown place' + row[1] + ' (' + row[0] + ')')

myPlaces = [ 'E92000001' ]

print('Reference date: ' + str(newest))
today=(newest - jan1).days
for code in myPlaces:
    place = places[code]
    print(place.format(today))

england = places['E92000001']
threshold = england.rateOverInterval(today, 7) * 4

for place in places:
    if (places[place].rateOverInterval(today, 7) > threshold):
        print(places[place].format(today))

with open('places.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([ 'Code', 'Name', 'Population', '1/1/2020' ])
    for place in places:
        data = [ places[place].code, places[place].name, places[place].population ]
        data.extend(places[place].cases)
        writer.writerow(data)
