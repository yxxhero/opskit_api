import multiprocessing
import os
import gevent.monkey
gevent.monkey.patch_all()


debug = True
timeout = 90
proc_name = 'opskit_api'
default_proc_name = 'opskit_api'
loglevel = 'debug'
bind = "0.0.0.0:5000"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
daemon = True
reload = True

workers = multiprocessing.cpu_count() * 2
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
