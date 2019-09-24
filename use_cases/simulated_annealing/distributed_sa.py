
import rpyc


def noisy(integer):
    return integer * 5


proxy = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})
linecount = proxy.root.line_counter(4, noisy)
print('The number of lines in the file was', linecount)