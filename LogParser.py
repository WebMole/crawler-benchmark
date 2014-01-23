import datetime # Used in evaluated log line

class LogParser(object):
    def __init__(self, log_file):
        self.log_file = log_file

    # We shouldn't do this :|
    def get_logged_times(self):
        data = []
        for line in self.log_file:
            data.append(eval(line))

        return data


if __name__ == '__main__':
    input_file_name = "logging.log"
    log_parser = LogParser(open(input_file_name, "r"))
    print log_parser.get_logged_times()



