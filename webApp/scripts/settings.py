# The point of this file is to remember data, as global variable works only inside a same file
# Thus, everytime we want a global variable for the whole programm, we will store it in d
# The value of a variable will be the value in d with as a key the string of the name of the variable

try:
    d
except:
    d = dict()

class Quisertarien():
    def __init__(self):
        pass
a = Quisertarien()

# The variable a is used so that we don't have to specify when we don't want add things.

def global_variable(name, value = a, delete = False):
    global d
    if delete:
        d.pop(name)
    if value == a:
        return d[name]
    else:
        d[name] = value