try:
    d
except:
    d = dict()


def global_variable(name, value = None, delete = False):
    global d
    if delete:
        d.pop(name)
    if value == None:
        return d[name]
    else:
        d[name] = value
