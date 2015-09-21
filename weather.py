import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mpldates
from matplotlib.ticker import MultipleLocator
from datetime import datetime
import csv
import glob

path = 'csv-files/*.csv'


def parse(rawfile, delimiter):
    """ Parses a raw csv file to a JSON-like object """

    opened_file = open(rawfile)
    rawdata = csv.reader(opened_file, delimiter=delimiter)
    parsed_data = []
    categories = rawdata.next()

    for row in rawdata:
        parsed_data.append(dict(zip(categories, row)))
    opened_file.close()

    return parsed_data




def monthly_mean(docum):
    """ Visualize daily Mean Temperature by date """

    parsed = parse(docum, ',')

    # From parsed data we keep the date 'EEST' and the temperature
    # 'Mean TemperatureC' in a dictionary. Also transforming the date
    # into a datetime object and the temperature into an integer.
    mean_temps = {datetime.strptime(item['EEST'], '%Y-%m-%d'):
                    int(item['Mean TemperatureC']) for item in parsed}

    # Sorting dates by turning the dictionary into a list of tuples
    mean_temps_tup = [(date, temp) for date, temp in mean_temps.items()]
    mean_temps_tup.sort()

    # Splitting into two lists in order to make plot
    dates, temps = zip(*mean_temps_tup)

    fig, ax = plt.subplots()

    f = ax.plot(dates, temps, color='royalblue')

    # Customizing appearance
    plt.ylabel('Mean Temperature C')
    plt.xticks(rotation=90, color='grey')
    plt.yticks(np.arange(13, 31), color='firebrick')
    plt.subplots_adjust(bottom=0.2)
    plt.grid()
    minorLocator = MultipleLocator(1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.rcParams['font.size'] = 8

    # Saving figure and closing
    plt.savefig('%s.png' % (str(docum)))
    plt.clf()

def run():
    for f in glob.glob(path):
        print 'Processing ' + f.split('/')[-1]
        monthly_mean(f)

run()

#monthly_mean(F2000)
#monthly_mean(F2001)
