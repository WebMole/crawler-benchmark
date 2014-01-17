# Custom http request for the JSON logging.

class LoggingRequest(object):


    def __init__(self, datetime, method, path, args, form, routing_exception, user_agent):
        self.datetime = datetime
        self.method = method
        self.path = path
        self.args = args
        self.form = form
        self.routing_exception = routing_exception
        self.user_agent = user_agent