import rpyc


class MyService(rpyc.Service):
    def exposed_line_counter(self, fileobj, function):
        var = function(fileobj)
        print('Hola')
        return var


from rpyc.utils.server import ThreadedServer
t = ThreadedServer(MyService, port = 18861)
t.start()