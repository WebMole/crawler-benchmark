import datetime # Used in evaluated log line
import re

# We shouldn't do this :|
def get_log_dicts(user_agent = None):
    log_file=open("logging.log", "r")
    requests = []
    for line in log_file:
        request = eval(line)
        if user_agent is not None:
            if re.match(user_agent, request['user_agent']):
                requests.append(request)
        else:
            requests.append(request)
    log_file.close()
    return requests


if __name__ == '__main__':
    print get_log_dicts()
