from __future__ import print_function
import datetime
import matplotlib.pyplot as plt

import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import LogParser
from matplotlib import ticker

import random

graph_colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k']

def timeTicks(x, pos):
    return "{:10.2f}".format(float(x) / 1.0)

formatter = ticker.FuncFormatter(timeTicks)

def get_total_seconds(td): return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

def timeDelta(dt1, dt2):
    #t1_ms = (dt1.hour*60*60 + dt1.minute*60 + dt1.second)*1000 + dt1.microsecond
    #t2_ms = (dt2.hour*60*60 + dt2.minute*60 + dt2.second)*1000 + dt2.microsecond
    #return max([t1_ms, t2_ms]) - min([t1_ms, t2_ms])
    return get_total_seconds(max([dt1, dt2]) - min([dt1, dt2]))

def draw_custom_graph(user_agents):
    plotXY = []

    #requests = LogParser.get_log_dicts(user_agent = r'SiteSucker.*')
    for user_agent in user_agents:
        requests = LogParser.get_log_dicts(user_agent = user_agent)
        firstDate = None
        x = []
        y = []
        for index, request in enumerate(requests):
            if index is not 0:
                x.append(timeDelta(request['datetime'], firstDate))
            else:
                firstDate = request['datetime']
                x.append(0)
            y.append(index)
        plotXY.append({'x':x, 'y':y})

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    currentIndex = 0;
    for xy in plotXY:
        # todo: Use different color (not only random) and add the ability to choose multiple user_agent.
        ax.plot(xy['x'], xy['y'], color=graph_colors[currentIndex % len(graph_colors)])
        currentIndex+=1

    plt.xlabel('Time (seconds)')
    plt.ylabel('Request number')

    ax.xaxis.set_major_formatter(formatter)

    output = StringIO.StringIO()
    canvas = FigureCanvas(fig)
    canvas.print_svg(output)
    return output