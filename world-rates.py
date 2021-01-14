#!/usr/bin/env python3

import codecs
import csv
import datetime
from contextlib import closing
import requests

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

name_col = 2
date_col = 3
newc_col = 5
vacc_col = 34
popn_col = 40

jan1 = datetime.date(2020, 1, 1)

class Country:
  def __init__(self, name, population):
    self.population = population
    self.name = name
    self.vaccinations = 0
    self.cases = []
    self.vaccinationDate = 0
  def addCases(self, daynum, num, vaccinations):
    while (len(self.cases) <= daynum):
      self.cases.append(0)
    if vaccinations > self.vaccinations:
      self.vaccinations = vaccinations
      self.vaccinationDate = daynum
    self.cases[daynum] = num
  def totalCases(self):
    return sum(self.cases)
  def days(self):
    return len(self.cases)
  def rateOverInterval(self, end, days):
    return sum(self.cases[end - days + 1:end + 1]) / self.population * 100000
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
    result += ', Ref Day: '
    result += str(jan1 + datetime.timedelta(day))
    return result

countries = {}
latestDay = 0
with closing(requests.get(url, stream=True)) as r:
  reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
  head = next(reader) # skip header
  for row in reader:
    country = row[name_col]
    if country == "International":
      continue
    if not country in countries:
      try:
        countries[country] = Country(country, float(row[popn_col]))
      except:
        print(country)
    row_date = datetime.datetime.strptime(row[date_col], '%Y-%m-%d').date()
    if row[vacc_col] == "":
      vaccinations = 0.0
    else:
      vaccinations = float(row[vacc_col])
    if row_date >= jan1:
      if (row_date - jan1).days > latestDay:
        latestDay = (row_date - jan1).days
      cases = row[newc_col]
      if cases == '':
        cases = 0
      else:
        cases = int(float(cases))
      if cases != 0:
        countries[country].addCases((row_date - jan1).days, cases, vaccinations)


print("Infection rates")
sortedCountries = sorted(countries, key=lambda place: countries[place].rateOverInterval(countries[place].days() - 1,7), reverse=True)
index = 0
printed = 0
while printed < 15:
  place = sortedCountries[index]
  if countries[place].days() > latestDay - 7:
    printed += 1
    print(countries[place].format(countries[place].days() - 1))
  index += 1
print()
print(countries["United Kingdom"].format(countries[place].days() - 1))
print(countries["France"].format(countries[place].days() - 1))
print(countries["Italy"].format(countries[place].days() - 1))
print(countries["Germany"].format(countries[place].days() - 1))

print()
print("Vaccination rates")
sortedCountries = sorted(countries, key=lambda place: countries[place].vaccinations / countries[place].population, reverse=True)
for place in sortedCountries[:15]:
  print(countries[place].name + 
          " percent vaccinated: " +
          f'{countries[place].vaccinations / countries[place].population * 100.0 :.2f}' +
          " total vaccinations: " +
          str (countries[place].vaccinations) +
          ' as of : ' +
          str(jan1 + datetime.timedelta(countries[place].vaccinationDate)))
