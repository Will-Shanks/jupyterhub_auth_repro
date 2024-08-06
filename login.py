#!/usr/bin/env python3

from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time
from timeit import default_timer as timer 

URL = "http://localhost:8000"
MAX_WORKERS=12

def login_as(i):
    #print("starting {}".format(i))
    jar = requests.cookies.RequestsCookieJar()
    r = requests.get(URL+"/hub/login?next=/hub/", cookies=jar)
    soup = BeautifulSoup(r.text, 'html.parser')
    xsrf = soup.find('input', attrs = {'name':'_xsrf'})['value']
    jar.set("_xsrf", xsrf)

    r = requests.post(URL+"/hub/login?next=/hub/", cookies=jar, data={"_xsrf":xsrf, "username":"foo"+str(i), "password":"bar"+str(i)})
    #print ("{}: {}".format(i, r.status_code))
    if r.status_code != 200:
        print(r.text)
    #print("done with {}".format(i))


def main():
    times = [[] for _ in range(MAX_WORKERS)]
    for _ in range(3):
        for j in range(1,MAX_WORKERS+1):
            start = timer()
            with concurrent.futures.ProcessPoolExecutor(max_workers=j) as p:
                p.map(login_as, [x for x in range(1, 21)])
            end = timer()
            delta = end - start
            print("{}, {}".format(j, delta))
            times[j-1].append("{:.2f}".format(delta))
    for j in range(MAX_WORKERS):
        print("{}, {}".format(j+1, ", ".join(times[j])))

    return 0

if "__main__" == __name__:
    import sys
    sys.exit(main())
