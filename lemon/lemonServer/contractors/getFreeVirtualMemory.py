import os

def get_value():
    result = []
    cmd = "WMIC OS GET FreeVirtualMemory /VALUE "
    response = os.popen(cmd + ' 2>&1','r').read().strip().split('=')
    return int(response[1])

if __name__ == '__main__':
    print(get_value())