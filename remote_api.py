import requests,re
import pythonmonkey as pm


class remote:
    def __init__(self):
        self.host_url = "http://messages.wuaze.com"
        self.headers = {
            "Accept": "application/json",
            #"Cookie": "__test= 160410ea18c85408ec8948efd1ca6262",
            "Cookie": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        self.update_header_cookie()
    
    def post(self,data:dict,url:str = None) -> dict:
        if url is None:
            url = self.host_url + "/api.php"

        try:
            response = requests.post(url,json=data, headers=self.headers)
            print(data,"->",response.text)
            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    pass
                    # if self.update_header_cookie(): 
                    #     return self.post(data,url)
        except:
            if self.update_header_cookie(): 
                return self.post(data,url)
        return {}

    def update_header_cookie(self) -> bool:
        def request_text(url,headers):
            headers["Cookie"] = ""
            while True:
                try:
                    response = requests.get(url,headers=headers)
                    if response.status_code == 200:
                        return str(response.text)
                    else:
                        return ""
                except requests.ConnectionError as e:
                    try:
                        response = requests.get("https://google.com/")
                        sleep(1)
                    except:
                        return ""

        js_part_1 = request_text(self.host_url+"/aes.js",self.headers)
        if js_part_1 == "":
            return False
        js_part_2 = ""
        try:
            pattern = r'<script\b[^>]*>(.*?)</script>'
            matches = re.findall(pattern, str(request_text(self.host_url,self.headers)), re.DOTALL)
        except:
            matches = []
        for script in matches:
            js_part_2 += script
        if js_part_2 == "":
            return False
        js_part_2 = js_part_2.replace("document.cookie=","return")
        to_run = js_part_1 + js_part_2
        try:
            runner = pm.eval("() =>{"+str(to_run)+"}")
            cookie = runner().split(';', 1)[0]
            self.headers["Cookie"] = str(cookie)
            return True
        except:
            return False
        return False

    def login(self,user,pasw) -> bool:
        self.update_header_cookie()
        data = {
            "command": "login",
            "user": user,
            "pasw": pasw
        }
        response = self.post(data)
        if "allow" in response:
            return response["allow"]
        return False

    def signup(self,user,pasw) -> bool:
        self.update_header_cookie()
        data = {
            "command": "signup",
            "user": user,
            "pasw": pasw
        }
        response = self.post(data)
        print(response)
        if "allow" in response:
            return response["allow"]
        return False
    
    def message(self,user,to,message) -> bool:
        data = {
            "command": "message",
            "user": user,
            "to": to,
            "message":message
        }
        response = self.post(data)
        if "allow" in response:
            return response["allow"]
        return False
    
    def get_message(self,user) -> bool:
        data = {
            "command": "get_message",
            "user": user,
        }
        response = self.post(data)
        if "messages" in response:
            return response["messages"]
        return []