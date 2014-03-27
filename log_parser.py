# noinspection PyUnresolvedReferences
import datetime  # Used in evaluated log line


def get_log_dicts(user_agent=None):
    log_file = open("logging.log", "r")
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


def clear_log(user_agents=None):
    # Read the log file
    log_file = open("logging.log", "r")
    lines = log_file.readlines()
    log_file.close()
    # ReWrite to the log file each lines excepts theses with selected user_agents
    log_file = open("logging.log", "w")
    for line in lines:
        has_to_write_line = True
        request = eval(line)
        if user_agents is not None:
            for user_agent in user_agents:
                if user_agent == request['user_agent']:
                    has_to_write_line = False
                    break
        if has_to_write_line:
            log_file.write(line)
    log_file.close()


def get_log_user_agents():
    log_file = open("logging.log", "r")
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
