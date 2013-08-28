'''
Created on 23.08.2013

@author: vau
'''
import json
import os

poll     = {
            'process':[
                   'Caption',
                   'CommandLine',
                   'CreationClassName',
                   'CreationDate',
                   'CSCreationClassName',
                   'CSName',
                   'Description',
                   'ExecutablePath',
                   'ExecutionState',
                   'Handle',
                   'HandleCount',
                   'InstallDate',
                   'KernelModeTime',
                   'MaximumWorkingSetSize',
                   'MinimumWorkingSetSize',
                   'Name',
                   'OSCreationClassName',
                   'OSName',
                   'OtherOperationCount',
                   'OtherTransferCount',
                   'PageFaults',
                   'PageFileUsage',
                   'ParentProcessId',
                   'PeakPageFileUsage',
                   'PeakVirtualSize',
                   'PeakWorkingSetSize',
                   'Priority',
                   'PrivatePageCount',
                   'ProcessId',
                   'QuotaNonPagedPoolUsage',
                   'QuotaPagedPoolUsage',
                   'QuotaPeakNonPagedPoolUsage',
                   'QuotaPeakPagedPoolUsage',
                   'ReadOperationCount',
                   'ReadTransferCount',
                   'SessionId',
                   'Status',
                   'TerminationDate',
                   'ThreadCount',
                   'UserModeTime',
                   'VirtualSize',
                   'WindowsVersion',
                   'WorkingSetSize',
                   'WriteOperationCount',
                   'WriteTransferCount'
                   ],
            'win32_perfformatteddata_perfproc_process':[
                    'Name',
                    'PercentProcessorTime',
                    'CreatingProcessID',
                    'HandleCount',
                    'IDProcess',
                    'ThreadCount',
                    'WorkingSet'                                     
                    ]
                
            }
 
def get_value(poll):     
    t_cmd = "wmic {0} get {1} /value"
    result  = {}
    for key, vlist in poll.items():
        param = key
        if key[0:6] == 'win32_':
            param   = 'path '+key
        cmd         = t_cmd.format(param,",".join(vlist))
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
    
    for p in result['win32_perfformatteddata_perfproc_process']:
        for v in result['process']:
            if p['IDProcess'] == v['ProcessId']:
                for _k,_v  in p.items():
                    v[_k] = _v
    result.pop('win32_perfformatteddata_perfproc_process')
    return json.dumps(result)     
if __name__ == '__main__':
    print(get_value(poll))