from secret import Secret
from requests import Request, Session
import json

class RCException(Exception):
    def __init__(self, reason=""):
        self.reason = reason

    def __repr__(self):
        return f'RCException("{self.reason}")'
    
def json_is_empty_list(data):
    isinstance(data,list) and len(data) == 0
   

class ResearchCollector:
    rcurl = 'https://www.researchcatalogue.net'

    def __init__(self): 
        self.session = Session()

    def login(self, username, password):
        rtext = self._post(
            "/session/login", data=dict(username=username, password=password))
        if rtext.strip():
            raise RCException("login failed")

    def logout(self):
        self._get("/session/logout")
    
    def get_research_as_json(self,url: str,params=None):
        page = 0
        results = []
        while (page < 20):
            print('page:\n', page)
            params["page"] = page
            resp = self._get(url,params)
            if resp == "[]":
                return results
            else:
                try:
                    data = json.loads(resp)
                except ValueError:
                    print (f"invalid json: {resp}")
                page = page + 1
                results = results + data
        print('careful, reached max page limit!')
        return results
            
    def _get(self, url, params=None):
        r = self.session.get(f"{self.rcurl}{url}", params=params)
        self.last_response = r
        if r.status_code != 200:
            raise RCException(
                f'GET {url} failed with status code {r.status_code}')
        return r.text
    
    def _post(self, url, data=None, files=None, headers=None):
        r = self.session.post(f"{self.rcurl}{url}",
                              data=data, files=files, headers=headers)
        self.last_response = r
        if r.status_code != 200:
            raise RCException(
                f'POST {url} failed with status code {r.status_code}')
        return r.text
    
rcol = ResearchCollector()
rcol.login(username=Secret.username,password=Secret.pw)

url = "/portal/search-result"
kcpedia = {
    "fulltext": "",
    "title": "",
    "autocomplete": "",
    "keyword": "kcpedia",
    "portal": "",
    "statusprogress": [0, 1],
    "statuspublished": [0, 1],
    "includelimited": [0, 1],
    "includeprivate": 0,
    "type_research": "research",
    "resulttype": "research",
    "modifiedafter": "",
    "modifiedbefore": "",
    "format": "json",
    "limit": 25,
    "page": 0
}

published = {
    'fulltext': '',
    'title': '',
    'autocomplete': '',
    'keyword': '',
    'portal': '6',
    'statusprogress': '0',
    'statuspublished': '1',
    'includelimited': '1',
    'includeprivate': '0',
    'type_research': 'research',
    'resulttype': 'research',
    'format': 'json',
    'limit': 50,
    'page': '0'
}

lectorate = {
    'fulltext': '',
    'title': '',
    'autocomplete': '',
    'keyword': 'KonCon Lectorate',
    'portal': '',
    'statusprogress': '1',
    'statuspublished': '1',
    'includelimited': '1',
    'includeprivate': '0',
    'type_research': 'research',
    'resulttype': 'research',
    'format': 'json',
    'limit': '50',
    'page': '0'
}

sonology = {
    'fulltext': '',
    'title': '',
    'autocomplete': '',
    'keyword': 'sonology',
    'portal': '6',
    'statusprogress': '1',
    'statuspublished': '1',
    'includelimited': '1',
    'includeprivate': '0',
    'type_research': 'research',
    'resulttype': 'research',
    'format': 'json',
    'limit': '50',
    'page': '0'
}

teachers = {
    'fulltext': '',
    'title': '',
    'autocomplete': '',
    'keyword': 'Research by teachers of the Royal Conservatoire',
    'portal': '',
    'statusprogress': '1',
    'statuspublished': '1',
    'includelimited': '1',
    'includeprivate': '0',
    'type_research': 'research',
    'resulttype': 'research',
    'format': 'json',
    'limit': '50',
    'page': '0'
}

all_params = [published,lectorate,sonology,teachers] 

data = []

for param in all_params:
    data = data + rcol.get_research_as_json(url,param)
    print("data:\n",data)

# save this data as a json string
with open('internal_research.json', 'w') as outfile:
    json.dump(data, outfile)
    outfile.close()








