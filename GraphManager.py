'''import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

import LogParser

def draw_custom_graph():

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    requests = LogParser.get_log_dicts()
    ys = range(0, len(requests))
    xs = [request['datetime'] for request in requests]

    axis.plot(xs, ys)

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    return output'''

from __future__ import print_function
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter

import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import LogParser

# every minutes
minutes   = MinuteLocator()

# every hour
hours     = HourLocator()
hoursFmt  = DateFormatter("%H:%M:%S")

def draw_custom_graph():
    #quotes = quotes_historical_yahoo('INTC', date1, date2)
    requests = LogParser.get_log_dicts(user_agent = r'SiteSucker*.')
    # todo: Eventually use the timedelta... Hell yeah!
    #firstDate = None
    #for request in requests:
    #    if firstDate is None:
    #        firstDate = request['datetime']
    #    request['datetime'] = request['datetime'] - firstDate

    #if len(quotes) == 0:
    #    print ('Found no quotes')
    #    raise SystemExit

    dates = [q['datetime'] for q in requests]
    opens = range(0, len(requests)) #[q[1] for q in quotes]

    fig, ax = plt.subplots()
    ax.plot_date(dates, opens, '-', color=[1, 0, 0])

    # Lambda Here to filter data...

    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hoursFmt)
    ax.xaxis.set_minor_locator(minutes)

    ax.autoscale_view()
    #ax.xaxis.grid(False, 'major')
    #ax.xaxis.grid(True, 'minor')
    ax.grid(True)

    fig.autofmt_xdate()

    #plt.show()

    output = StringIO.StringIO()
    canvas = FigureCanvas(fig)
    #canvas.print_png(output)
    canvas.print_svg(output)
    return output
