# -*- coding: utf-8 -*-
import StringIO

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import ticker

from project.tools import logger

graph_colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']


def time_ticks(x, pos):
    return "{:10.2f}".format(float(x) / 1.0)


formatter = ticker.FuncFormatter(time_ticks)


def get_total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


def time_delta(dt1, dt2):
    return get_total_seconds(max([dt1, dt2]) - min([dt1, dt2]))


def draw_custom_graph(user_agents):
    plot_x_y = []

    # requests = log_parser.get_log_dicts(user_agent = r'SiteSucker.*')
    for user_agent in user_agents:
        requests = logger.get_log_dicts(user_agent=user_agent)
        first_date = None
        x = []
        y = []
        for index, request in enumerate(requests):
            if index is not 0:
                x.append(time_delta(request['datetime'], first_date))
            else:
                first_date = request['datetime']
                x.append(0)
            y.append(index)
        plot_x_y.append({
            'x': x,
            'y': y
        })

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    current_index = 0
    for xy in plot_x_y:
        # todo: Use different color (not only random) and add the ability to choose multiple user_agent.
        ax.plot(
            xy['x'], xy['y'],
            color=graph_colors[current_index % len(graph_colors)],
            label=user_agents[current_index]
        )
        ax.legend(framealpha=0.5, loc=4, prop={'size': 8})
        current_index += 1

    plt.xlabel('Delta Time (seconds)')
    plt.ylabel('Number of requests')

    ax.xaxis.set_major_formatter(formatter)

    output = StringIO.StringIO()
    canvas = FigureCanvas(fig)
    canvas.print_svg(output)
    return output