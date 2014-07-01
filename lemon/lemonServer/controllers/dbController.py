# DataBase controller
# Handling requests to db
#
#
import core
import json
import re
import urllib

# getting key from database
# query params: collection, key
def get( req, res):
    pass

# params: 
# "name" - name of DataItem. If name ==  null return ALL DataItems

'''
    params:
    id = mongodb _id of DataItem
    name = name of DataItem. Returned list of DataItems
    datafrom = timestamp which is begin timestamp of data to return
    datato   = timestamp of end data for to return
''' 
def getDataItem( req, res ):
    _id     = req.query.get('id',[''])[0]
    print(_id)
    name    = req.query.get('name',[''])[0]
    datafrom= req.query.get('datafrom',[''])[0]
    datato  = req.query.get('datato',[''])[0]
    print(name)
    print(datafrom)
    print(datato)
    res.send_json({})

