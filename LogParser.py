import datetime # Used in evaluated log line

# We shouldn't do this :|
def get_log_dicts(log_file=open("logging.log", "r")):
    data = []
    for line in log_file:
        data.append(eval(line))
    return data


if __name__ == '__main__':
    print get_log_dicts()



