import os

def get_cpu_load():
    """ Returns a list CPU Loads"""
    result = []
    cmd = "WMIC CPU GET LoadPercentage "
    response = os.popen(cmd + ' 2>&1','r').read().strip().splitlines()
    for load in response[2:]:
        result.append(int(load))
    return result[0]

if __name__ == '__main__':
    print(get_cpu_load())