import os

directory = '/home/ugrads/l/lweichel13/Work/repos/pythontrial/user-service'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        os.remove(filename)

directory = '/home/ugrads/l/lweichel13/Work/repos/pythontrial/social-graph-service'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        os.remove(filename)

directory = '/home/ugrads/l/lweichel13/Work/repos/pythontrial/nginx-web-server'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        os.remove(filename)

directory = '/home/ugrads/l/lweichel13/Work/repos/pythontrial/jaeger-query'
for filename in os.scandir(directory):
    if filename.name.endswith('.json'):
        os.remove(filename)
