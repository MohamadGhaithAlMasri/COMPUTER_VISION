import urllib.request
import http

base = "http://192.168.135.234/"


def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n

    except http.client.HTTPException as e:
        return e


#two = transfer("two")
#one = transfer("one")
#print(one, two)
#value = transfer("45")   #Send this data

#you can send pwm255 and then decode it to get pwm or more varibales