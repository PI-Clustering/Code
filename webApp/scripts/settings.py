try:
    d
except:
    d = dict()

class Quisertarien():
    def __init__(self):
        pass
a = Quisertarien()

def global_variable(name, value = a, delete = False):
    global d
    if delete:
        d.pop(name)
    if value == a:
        return d[name]
    else:
        d[name] = value