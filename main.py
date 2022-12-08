#### Pingator
appver = "3.7.2"
appname = "Pingator microservice"
appshortname = "Pingator"
from prometheus_client import start_http_server, Gauge
from time import sleep as sleep
from datetime import datetime
import ping3
import requests


print("Version "+appver)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
tab='  |'
get_delay=10
ping3.EXCEPTIONS = True
server_port = 80

APP_INFO = Gauge('app_info', 'Return app info',['appname','appshortname','version'])
PING_TIME = Gauge('ping_time_host', 'Return time ping to host',['ping_host'])
GET_RESPONCE = Gauge('responce_from_url', 'Responce from url',['url'])

APP_INFO.labels(appname,appshortname,appver).set(1)

def get_date_time():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return(date_time)
def ping_gauge(host):
    try:
      result = ping3.ping(host, unit='ms')
    except ping3.errors.HostUnknown:  # Specific error is catched.
        print(tab+get_date_time()+' '+host+' '+"Host unknown error raised.")
        result = 9999
    except ping3.errors.PingError:  # All ping3 errors are subclasses of `PingError`.
        print(tab+get_date_time()+' '+host+' '+"A ping error raised.")
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
        print(tab+get_date_time()+' '+ host +' '+str(result))
        PING_TIME.labels(host).set(result)

def get_url_responce(url):
    try:
        responce = requests.get(url,verify=False)
        responce_code = responce.status_code
        responce.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(tab +get_date_time()+' '+url + ' '  +" :Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        responce_code=500
        print(tab +get_date_time()+' '+url + ' '  + " :Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        responce_code = 500
        print(tab +get_date_time()+' '+url + ' '  + " :Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        responce_code = 500
        print(tab +get_date_time()+' '+url + ' '  + " :OOps: Something Else", err)

    return(responce_code)

def get_urls_responces():
    urllistfile = 'urllist.txt'
    with open(urllistfile, 'r') as text:
        urls = text.readlines()
    urls = [line.rstrip() for line in urls]
    print('Get responce from ' + urllistfile + ' ......')

    for url in urls:
        result = get_url_responce(url)
        print(tab+get_date_time()+' ' +url +' ' +str(result))
        GET_RESPONCE.labels(url).set(result)

if __name__ == '__main__':
    start_http_server(server_port)
    while True:
      get_ping_time()
      get_urls_responces()
      print('----------------------------')
      sleep(get_delay)
