import os
import json

poll     = {
                'os':['Caption',
                       'Version',
                       'LastBootUpTime' 
                       ],
                'computersystem': ['Caption', 
                       'DNSHostName', 
                       'Domain', 
                       'Manufacturer', 
                       'Model', 
                       'Name',
                       'NumberofLogicalProcessors', 
                       'NumberOfProcessors', 
                       'Status'],
                'cpu': ['Name',
                        'NumberOfCores',
                        'NumberOfLogicalProcessors',
                        'MaxClockSpeed',
                        'Manufacturer',
                        'CurrentClockSpeed',
                        'AddressWidth',
                        'DataWidth',
                        'Caption',
                        'Description'
                        ],
                'logicaldisk': ['Caption',
                                'FreeSpace',
                                'Description']
                 }

def get_value(poll):     
    t_cmd = "wmic {0} get {1} /value"
    result  = {}
    for key, vlist in poll.items():
        cmd         = t_cmd.format(key,",".join(vlist))
        response    = os.popen(cmd + ' 2>&1','r').read().strip().splitlines()
        result[key] = []
        line        = {}
        for v in response:
            row = v.split('=')
            if len(row) > 1:
                try:
                    if line[row[0]] is not None:
                        result[key].append(line)
                        line    = {}
                except KeyError:
                    pass                    
                line[row[0]] = row[1]
        result[key].append(line)
    return json.dumps(result)            
    
    
if __name__ == '__main__':
    print(get_value(poll))