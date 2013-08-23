import os

def get_value():
    cmd = "WMIC OS GET FreePhysicalMemory /VALUE"
    response = os.popen(cmd + ' 2>&1','r').read().strip().split('=')
    free    = int(response[1])*1024;
    cmd = "WMIC computersystem GET TotalPhysicalMemory /VALUE"
    response = os.popen(cmd + ' 2>&1','r').read().strip().split('=')
    total   = int(response[1]);
    return total - free;

if __name__ == '__main__':
    print(get_value())