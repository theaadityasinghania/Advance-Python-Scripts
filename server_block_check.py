import netifaces
import pycurl
from io import BytesIO
import json

def curl_post(url, iface=None):
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(c.URL, url)
    c.setopt(c.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0")
    c.setopt(c.TIMEOUT, 10)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    if iface:
        c.setopt(c.INTERFACE, iface)
    c.perform()

    # Json response
    resp = buffer.getvalue().decode('iso-8859-1')

    #  Check response is a JSON if not there was an error
    try:
        resp = json.loads(resp)
    except json.decoder.JSONDecodeError:
        pass

    buffer.close()
    c.close()
    return resp


if __name__ == '__main__':
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != 'lo':
            res = curl_post("https://www.google.com/", interface)
            if res:
                print(interface, 'Working.')
            else:
                print(interface, 'Seems blocked.')
