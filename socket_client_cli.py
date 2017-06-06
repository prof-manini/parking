# -*- coding:utf-8 -*-

import cmd

class BaseCli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '

    def do_quit(self, arg):
        print "\nbye bye"
        return 1

    def do_EOF(self, arg):
        self.do_quit(None)
        return 1

    def emptyline(self):
        pass

    def run(self):
        self.cmdloop()

#
import cmd
from parking_simulation import SocketClient
class ParkSocketCli(BaseCli):

    def __init__(self):
        BaseCli.__init__(self)
        with open("port.txt") as file:
            self.port = int(file.read())

    def do_state(self, line):
        client = SocketClient(port=self.port)
        data = client.get_data()
        mess = "STATE: %s " % data
        print(mess)
        del client

def main(args):
    cli = ParkSocketCli()
    cli.run()

if __name__ == "__main__":

    import sys
    args = sys.argv[1:]
    sys.exit(main(args))
