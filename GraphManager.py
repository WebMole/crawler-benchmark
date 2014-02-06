import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

import LogParser

def draw_custom_graph():

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    requets = LogParser.get_log_dicts()
    ys = range(0, len(requets))
    xs = [request['datetime'] for request in requets]

    axis.plot(xs, ys)

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    return output