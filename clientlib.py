import requests
import logging
import json
from datetime import datetime
from datetime import date
from datetime import time

class FileUploadException(Exception):
    pass

class FileDownloadException(Exception):
    pass

class NotFound404(Exception):
    pass

class HTTPException(Exception):
    pass

class RestApiClient:
    def __init__(self, root_url="http://localhost:5000/api"):
        self.__session_id=None
        self.__cookies=None
        self.__root=f"{root_url}/v1.0"

    def login(self, username, password):
        headers={
            "username":username,
            "password":password
        }

        r=requests.post(f'{self.__root}/core/login', headers=headers)

        if r.status_code==200:
            session=r.cookies['session']
        else:
            session=None

        if r.status_code!=200:
            raise HTTPException(f"{r.text}")

        self.__cookies={"session": session}
        self.__session_id=session
        return r.text

    def logoff(self):
        r=requests.post(f'{self.__root}/core/logoff', cookies=self.__cookies)
        self.__session_id=None
        if r.status_code!=200:
            raise HTTPException(f"{r.text}")
        return r.text

    def delete(self, table, id,json_out=False):
        url=f"{self.__root}/data/{table}/{id}"
        r=requests.delete(url, cookies=self.__cookies)
        print(r.status_code)
        if r.status_code!=200:
            raise HTTPException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text

    def add(self, table,data,json_out=False):
        logging.warning("Method add ist deprecated! Pse use create")
        result= self.create(table,data,json_out)

        if json_out==True:
            return json.loads(result)
        else:
            return result

    def create(self, table,data,json_out=False):
        url=f"{self.__root}/data/{table}"
        headers={"Content-Type":"application/json"}
        data=json.dumps(data,default=self.__json_serial)
        data=json.loads(data)
        r=requests.post(url, headers=headers, json=data, cookies=self.__cookies)
        if r.status_code!=200:
            raise HTTPException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text

    def read(self, table, id,json_out=False):
        url=f"{self.__root}/data/{table}/{id}"
        r=requests.get(url, cookies=self.__cookies)
        if r.status_code!=200:
            raise NotFound404(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text

    def update(self,table,id, data,json_out=False):
        url=f"{self.__root}/data/{table}/{id}"
        headers={"Content-Type":"application/json"}
        data=json.dumps(data,default=self.__json_serial)
        data=json.loads(data)
        r=requests.put(url, headers=headers, json=data, cookies=self.__cookies)
        if r.status_code!=200:
            raise HTTPException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text

    def read_multible(self, table, fetchxml=None,json_out=False, none_if_eof=False, page=0, page_size=5000):
        if fetchxml==None:
            url=f"{self.__root}/data/{table}?page={page}&page_size={page_size}"
            r=requests.get(url, cookies=self.__cookies)
        elif type(fetchxml) is dict:
            clause=""

            for key, value in fetchxml.items():
                clause=f"""
                {clause}\n<condition field="{key}" value="{value}" operator="="/>
                """

            fetchxml=f"""
                <restapi type="select">
                <table name="{table}"/>
                <comment text="from clientlib.py (read_multible)"/>
                <filter type="AND">
                    {clause}
                </filter>
                </restapi>
                """

            url=f"{self.__root}/data?page={page}&page_size={page_size}"
            headers={"Content-Type":"application/xml"}
            r=requests.post(url, cookies=self.__cookies, data=fetchxml, headers=headers)
        else:
            url=f"{self.__root}/data?page={page}&page_size={page_size}"
            headers={"Content-Type":"application/xml"}
            r=requests.post(url, cookies=self.__cookies, data=fetchxml, headers=headers)

        if r.status_code!=200:
            raise HTTPException(f"{r.status_code} {r.text}")

        json_obj=json.loads(r.text)

        if none_if_eof and json_obj==[]:
            return None

        if json_out==True:
            return json_obj
        else:
            return r.text

    def execute_action(self,action_name,data,json_out=False):
        url=f"{self.__root}/action/{action_name}"
        headers={"Content-Type":"application/json"}
        data=json.dumps(data,default=self.__json_serial)
        data=json.loads(data)
        r=requests.post(url, headers=headers, json=data, cookies=self.__cookies)
        if r.status_code!=200:
            raise HTTPException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text


    def post_file(self,local_file, remote_path, json_out=False):
        #url=f"http://localhost:5000/api/v1.0/file/{path}"
        url=f"{self.__root}/file/{remote_path}"

        files={'file': open(local_file,'rb')}
        #values={'file' : 'file.txt' , 'DB':'photcat' , 'OUT':'csv' , 'SHORT':'short'}
        r=requests.post(url,files=files,data={})
        if r.status_code!=200:
            raise FileUploadException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text


    def put_file(self,local_file, remote_path, json_out=False):
        url=f"{self.__root}/file/{remote_path}"

        files={'file': open(local_file,'rb')}
        #values={'file' : 'file.txt' , 'DB':'photcat' , 'OUT':'csv' , 'SHORT':'short'}
        r=requests.put(url,files=files,data={})
        if r.status_code==404:
            raise FileUploadException(f"File not found. {r.status_code} {r.text}")

        if r.status_code!=200:
            raise FileUploadException(f"{r.status_code} {r.text}")

        if json_out==True:
            return json.loads(r.text)
        else:
            return r.text


    def get_file(self, remote_path, local_file_name, json_out=False):
        url=f"{self.__root}/file/{remote_path}"
        r=requests.get(url)

        if r.status_code!=200:
            raise FileDownloadException(f"{r.status_code} {r.text}")

        result={"file": r.content}


        #file_bytes=
        #attachment=json.loads(rest.read("api_attachment", 1))
        #import base64

        #base64_message = attachment['file']
        #base64_bytes = base64_message.encode('ascii')
        #message_bytes = base64.b64decode(base64_bytes)

        #f = open('/tmp/img.jpg', 'wb')
        #f.write(message_bytes)
        #f.close()

        return result

    def __json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))


if __name__=='__main__':
    client=RestApiClient()
    print(client.login("root", "password"))

    #print(client.delete("dummy",99))
    #print(client.delete("dummy",100))
    #print(client.add("dummy", {'id':99,'name':'IC735', 'port':3306}))
    #print(client.add("dummy", {'id':100,'name':'TEST', 'port':3306}))
    #print(client.read("dummy", 99))
    #print(client.update("dummy", 99, {'id':99,'name':'GD77', 'port':3307}))
    #print(client.read("dummy", 99))
    #print(client.read_multible("dummy"))


    dummies=client.read_multible("dummy", {"id": 1, "name":"test"}, json_out=True)
    print(dummies)

    fetch="""
    <restapi type="select">
        <table name="dummy"/>
        <comment text="from admin.py"/>
        <filter type="OR">
            <condition field="name" value="GD77" operator="="/>
            <condition field="name" value="TEST" operator="="/>
        </filter>
    </restapi>
    """
    #dummies=client.read_multible("dummy", fetch, json_out=True)
    #for dummy in dummies:
    #    print(dummy)

    #print("Executing a test action ...")
    #print(client.execute_action('test',{"id":"12345"}))

    print(client.logoff())



