#curl -sS -i -X POST -H 'Content-Type: application/json-rpc' -d '{"params": {"password": "Nik9640707", "user": "Alexander"}, "jsonrpc":"2.0", "method": "user.login", "id": 1, "auth":null}' http://mail.tor-service.ru/zabbix/api_jsonrpc.php
#https://www.zabbix.com/documentation/3.0/ru/manual/api
import requests
import json
import sys

from peewee import long


class ZABBIX():

    s = requests.Session()
    def __init__(self):
        self.url = 'http://192.168.10.30/zabbix/api_jsonrpc.php'
        self.headers = {
            'Content-Type': 'application/json-rpc'
        }
        self.debug = True
        self.__result = []
        self.items_43 = ['Desc 1', 'Cons PerCent 1', 'Desc 2', 'Cons PerCent 2',
                      'Desc 3', 'Cons PerCent 3', 'Desc 4', 'Cons PerCent 4',
                      'Desc 5', 'Cons PerCent 5', 'Desc 6', 'Cons PerCent 6',
                      'Desc 7', 'Cons PerCent 7', 'Desc 8', 'Cons PerCent 8',
                      'Desc 9', 'Cons PerCent 9', 'Desc 10', 'Cons PerCent 10',
                      'Desc 11', 'Cons PerCent 11', 'Desc 12',
                      'Cons PerCent 12', 'Desc 13', 'Cons PerCent 13',
                      'Desc 14', 'Cons PerCent 14', 'Desc 15',
                      'Cons PerCent 15', 'Desc 16', 'Cons PerCent 16',
                      'Desc 17', 'Cons PerCent 17', 'Desc 18',
                      'Cons PerCent 18', 'Desc 19', 'Cons PerCent 19',
                      'Desc 20', 'Cons PerCent 20']


    def auth(self, login, password):


        data = {"params": {"password": password, "user": login}, "jsonrpc":"2.0", "method": "user.login", "id": 1, "auth":None}

        req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
        if (req.status_code == 200):
            js = json.loads(req.text)
            if self.debug == True:
                print (js)
            self.auth_code = (js['result'])
        else:
            print ('ошибка авторизаци ' + req.text)
      #      sys.exit(1)

    def get_id_groups(self, names):

        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                    "output":"groupid",
                     "filter": {
                    "name": names
                }
            },
            "auth": self.auth_code,
            "id": 3
        }
        try:
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"

            js = json.loads(req.text)
            temp = []
            for object in js['result']:
                temp.append(object['groupid'])
            return temp
        except Exception as ex:
            print(ex)



    def get_groups(self ):

        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output":"extend",

            },
            "auth": self.auth_code,
            "id": 3
        }
        try:
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"

            js = json.loads(req.text)
            return js['result']
        except Exception as ex:
            print(ex)

    def get_host(self, groupids):

        print (groupids)

        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output":["host"],
                "groupids": groupids,

            },
            "id": 2,
            "auth": self.auth_code
        }
        try:
            req = self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            if self.debug:
                print( req.text)
            js = json.loads(req.text)
            return js['result']
        except Exception as ex:
            print(ex)

    def get_item(self, hostids):

        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["name"],
                "hostids": hostids,

            },
            "id": 2,
            "auth": self.auth_code
        }
        try:
            req = self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            if self.debug:
                print( req.text)
            js = json.loads(req.text)
            return js['result']
        except Exception as ex:
            print(ex)


    def get_items(self, list):
        list_items = ["lastvalue", "lastclock", 'name']
        try:

            data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": list_items,

                    "itemids": list

                },
                "id": 4,
                "auth":   self.auth_code
            }
            #получаем 'Device Serial Number',
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            #if self.debug:
            print( req.text)
            js_items = json.loads(req.text)
            return js_items['result']
        except Exception as ex:
            print (ex)


    def get_host_groups(self, host, groupdid):
        list_items = ["lastvalue", "lastclock", 'name']
        hosts = self.get_host(groupdid)
        try:

            data = {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": list_items,
                        "application": "A41 General",
                        "hostids": 1

                    },
                    "id": 4,
                    "auth":   self.auth_code
                }
                #получаем 'Device Serial Number',
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            if self.debug:
                print( req.text)
            js_items = json.loads(req.text)
            for items in js_items['result']:
                if items['name'].find('Device Serial Number',) > -1:
                    if long(items['lastclock']) >0:
                        result_data['Device Serial Number'] = items['lastvalue']


            data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": list_items,
                        "application": "A43 Consumables",
                        "hostids": object['hostid']

                    },
                    "id": 4,
                    "auth":   self.auth_code
                }
                #получаем счетчики краски
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            if self.debug:
                print( req.text)
            js_items = json.loads(req.text)
            result_data['A43']={}
            for items in js_items['result']:

                for param in self.items_43:
                    if items['name'].find(param) > -1:
                        if long(items['lastclock']) >0:
                            result_data['A43'][items['name']] = items['lastvalue']

                #получаем простые счетчики

            data = {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": list_items,

                        "hostids": object['hostid'],
                        "application": "A42 Counters"

                    },
                    "id": 4,
                    "auth":   self.auth_code
                }
                #получаем счетчики краски
            req =  self.s.post(self.url, data=json.dumps(data), headers=self.headers) # this will make the method "POST"
            if self.debug:
                print( req.text)
            js_items = json.loads(req.text)
            result_data['A42']={}
            for items in js_items['result']:
                if long(items['lastclock']) >0:
                    result_data['A42'][items['name']] = items['lastvalue']

            self.__result.append(result_data)

        except Exception as ex:
            print (ex)
        return self.__result


    def clear(self):
        self.__result.clear()


