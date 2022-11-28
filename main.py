#### Pingator v.2.2
from prometheus_client import start_http_server, Gauge
import time
import ping3
import requests

tab='  |'
ping3.EXCEPTIONS = True

PING_TIME = Gauge('ping_time_host', 'Return time ping to host',['ping_host'])
GET_RESPONCE = Gauge('responce_from_url', 'Responce from url',['url'])

hostlist='hostlist.txt'
with open(hostlist, 'r') as text:
    hosts = text.readlines()
hosts = [line.rstrip() for line in hosts]

urllist='urllist.txt'
with open(urllist, 'r') as text:
    urls = text.readlines()
urls = [line.rstrip() for line in urls]
#header ={'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

def ping_gauge(h):
    try:
      x = ping3.ping(h, unit='ms')
    except ping3.errors.HostUnknown:  # Specific error is catched.
        print(tab+h+':'+"Host unknown error raised.")
        x = 9999
    except ping3.errors.PingError:  # All ping3 errors are subclasses of `PingError`.
        print(tab+h+':'+"A ping error raised.")
        x = 9999
    return(x)

def get_ping_time():
    print('Get ping time from '+hostlist+' ......')
    for host in hosts:
        ptime = ping_gauge(host)
        print(tab+host +':'+str(ptime))
        PING_TIME.labels(host).set(ptime)

def get_host_responce():
    print('Get responce from '+urllist+' ......')
    for url in urls:
        try:
            responce = requests.get(url)
            responce.raise_for_status()
            print(tab + url + ' :' + str(responce.status_code))
        except requests.exceptions.HTTPError as errh:
            print(tab +url+" :Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print(tab +url+" :Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print(tab +url+" :Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print(tab +url+" :OOps: Something Else", err)

        GET_RESPONCE.labels(url).set(responce.status_code)

if __name__ == '__main__':
    start_http_server(8000)
    while True:
      get_ping_time()
      get_host_responce()
      print('----------------------------')
      time.sleep(10)

