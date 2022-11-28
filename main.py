#### Pingator v.3.4
from prometheus_client import start_http_server, Gauge
from time import sleep as sleep
import ping3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
tab='  |'
get_delay=10
ping3.EXCEPTIONS = True
server_port = 8000

PING_TIME = Gauge('ping_time_host', 'Return time ping to host',['ping_host'])
GET_RESPONCE = Gauge('responce_from_url', 'Responce from url',['url'])

def ping_gauge(h):
    try:
      result = ping3.ping(h, unit='ms')
    except ping3.errors.HostUnknown:  # Specific error is catched.
        print(tab+h+':'+"Host unknown error raised.")
        result = 9999
    except ping3.errors.PingError:  # All ping3 errors are subclasses of `PingError`.
        print(tab+h+':'+"A ping error raised.")
        result = 9999
    return(result)

def get_ping_time():
    hostlistfile = 'hostlist.txt'
    with open(hostlistfile, 'r') as text:
        hosts = text.readlines()
    hosts = [line.rstrip() for line in hosts]
    print('Get ping time from '+hostlistfile+' ......')

    for host in hosts:
        result = ping_gauge(host)
        print(tab+host +':'+str(result))
        PING_TIME.labels(host).set(result)

def get_url_responce(url):
    try:
        responce = requests.get(url,verify=False)
        responce_code = responce.status_code
        responce.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(tab + url + ' '  +":Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print(tab + url + ' '  + " :Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print(tab + url + ' '  + " :Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print(tab + url + ' '  + " :OOps: Something Else", err)

    return(responce_code)

def get_urls_responces():
    urllistfile = 'urllist.txt'
    with open(urllistfile, 'r') as text:
        urls = text.readlines()
    urls = [line.rstrip() for line in urls]
    print('Get responce from ' + urllistfile + ' ......')

    for url in urls:
        result = get_url_responce(url)
        print(tab +url +' :' +str(result))
        GET_RESPONCE.labels(url).set(result)

if __name__ == '__main__':
    start_http_server(server_port)
    while True:
      get_ping_time()
      get_urls_responces()
      print('----------------------------')
      sleep(get_delay)
