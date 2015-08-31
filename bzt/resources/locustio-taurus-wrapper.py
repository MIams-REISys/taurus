#! /usr/bin/env python2
import csv
import os
import time

from locust import main, events

fname = os.environ.get("JTL")
if not fname:
    raise ValueError("Please specify JTL environment variable")


def getrec(request_type, name, response_time, response_length, exc=None):
    rc = '200' if exc is None else '500'
    rm = 'OK' if exc is None else '%s' % exc
    return {
        'ts': "%d" % time.time(),
        'label': name,
        'method': request_type,
        'elapsed': response_time,
        'bytes': response_length,  # NOTE: not sure if the field name is right
        'rc': rc,
        'rm': rm,
        'success': 'true' if exc is None else 'false'
    }


if __name__ == '__main__':
    with open(fname, 'wt') as fhd:
        writer = csv.DictWriter(fhd, getrec(None, None, None, None).keys())
        writer.writeheader()


        def on_request_success(request_type, name, response_time, response_length):
            writer.writerow(getrec(request_type, name, response_time, response_length))


        def on_request_failure(request_type, name, response_time, exception):
            writer.writerow(getrec(request_type, name, response_time, 0, exception))


        events.request_success += on_request_success
        events.request_failure += on_request_failure

        main.main()
