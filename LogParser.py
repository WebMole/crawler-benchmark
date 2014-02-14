import datetime # Used in evaluated log line
#import re

# We shouldn't do this :|
def get_log_dicts(user_agent = None):
    log_file=open("logging.log", "r")
    requests = []
    for line in log_file:
        request = eval(line)
        if user_agent is not None:
            #if re.match(user_agent, request['user_agent']):
            if user_agent == request['user_agent']:
                requests.append(request)
        else:
            requests.append(request)
    log_file.close()
    return requests

def get_log_user_agents():
    log_file=open("logging.log", "r")
    user_agents = []
    for line in log_file:
        request = eval(line)
        user_agent = request['user_agent']
        if user_agent not in user_agents:
            user_agents.append(user_agent)
    log_file.close()
    return user_agents

if __name__ == '__main__':
    print get_log_dicts()
