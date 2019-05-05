import getopt,socket,sys,re

class Scan:
    def __init__(self,args):
        self._getargs(args)
    def _getargs(self,args):
        opt = dict(getopt.getopt(args,'',['host=','port='])[0])
        host = opt.get('--host')
        host_match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',host)
        if not host_match:
            print('Parameter Error')
            sys.exit(-1)
        self.host = host
        port_str = opt.get('--port')
        port_l = port_str.split('-')
        port = []

        for i in port_l:
            if not i.isdigit():
                print('Parameter Error')
                sys.exit(-1)
        if len(port_l) == 1:
            port.append(int(port_l[0]))
        elif len(port_l) == 2:
            port = [ i for i in range(int(port_l[0]),int(port_l[1])+1)]

        self.port = port

    def start(self):
        for i in self.port:
            addr = (self.host,i)
            sk = socket.socket()
            ret = sk.connect_ex(addr)
            if ret:
                print('{} closed'.format(i))
            else:
                print('{} open'.format(i))
if __name__ == '__main__':
    scan = Scan(sys.argv[1:])
    scan.start()



