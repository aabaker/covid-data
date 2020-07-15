# covid-data
Code to extract interesting trends from UK government statistics

The script area-rates will pick out areas that exceed 4 times the average
case rate for the whole of England over the last week. If the list myPlaces
is set to a list of area codes it will also list rates for those areas.

The population data is culled from two ONS databases listed in the data-sources
file. Two sources were used as, due to council boundary changes, neither source
contained every authority that is used in the Covid data reporting.
