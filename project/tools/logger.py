# noinspection PyUnresolvedReferences
import datetime
import logging.config
import re

import yaml
from flask import request, g

from project import app
from project.configuration import Configuration
from project.models.LoggingRequest import LoggingRequest
from project.tools.tools import tail

logging.config.dictConfig(yaml.load(open(Configuration.log_conf_path)))
log_file = logging.getLogger('file')
logConsole = logging.getLogger('console')


def get_log_dicts(user_agent=None, path_regex=None, last_n_lines=None):
    log_file = open(Configuration.log_file_path, "r")
    requests = []
    if last_n_lines is not None:
        lines = tail(log_file, last_n_lines)[0]
    else:
        lines = log_file
    for line in lines:
        request = eval(line)
        has_to_append = True
        if user_agent is not None:
            if user_agent != request['user_agent']:
                has_to_append = False
        if path_regex is not None:
            if not re.match(path_regex, request['path'], re.M | re.I):
                has_to_append = False
        if has_to_append:
            requests.append(request)
    log_file.close()
    return requests


# @todo: Use this function to display something in results
def get_log_dicts_success():
    return get_log_dicts(path_regex=r'/success/(.*)')


def get_log_dicts_failure():
    return get_log_dicts(path_regex=r'/fail/(.*)')


def clear_log(user_agents=None):
    # Read the log file
    log_file = open(Configuration.log_file_path, "r")
    lines = log_file.readlines()
    log_file.close()

    # ReWrite to the log file each lines excepts theses with selected user_agents
    log_file = open(Configuration.log_file_path, "w")
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
    log_file = open(Configuration.log_file_path, "r")
    user_agents = []
    for line in log_file:
        request = eval(line)
        user_agent = request['user_agent']
        if user_agent not in user_agents:
            user_agents.append(user_agent)
    log_file.close()
    return user_agents


@app.after_request
def per_request_callbacks(response):
    if not re.match(r'/admin(.*)', request.path, re.M | re.I):

        for func in getattr(g, 'call_after_request', ()):
            response = func(response)

        lr = LoggingRequest(
            datetime.datetime.today(),
            request.method,
            request.path,
            request.args.lists(),
            request.form.lists(),
            None if request.routing_exception is None
            else str(request.routing_exception),
            get_http_user_agent()
        )

        str_to_log = lr.__dict__
        log_file.debug(str_to_log)

    return response


def get_http_user_agent():
    try:
        return request.environ['HTTP_USER_AGENT']
    except KeyError:
        return None


if __name__ == '__main__':
    print get_log_dicts()
