#ftp_server_auth.py
import os
 
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
 
FTP_HOST = '0.0.0.0'
FTP_PORT = 9021
 
FTP_ADMIN_DIR = os.path.join(os.getcwd(), 'uploads')
FTP_USERS_DIR = os.path.join(os.getcwd(), 'uploads/users')
FTP_ANONY_DIR = os.path.join(os.getcwd(), 'uploads/anonymous')
 
def main():
    authorizer = DummyAuthorizer()
    
    authorizer.add_user('admin', 'admin1234', FTP_ADMIN_DIR, perm='elradfmwMT')
    authorizer.add_user('dochi', 'dochi1234', FTP_USERS_DIR, perm='elr')
    authorizer.add_anonymous(FTP_ANONY_DIR)
 
    handler = FTPHandler
    handler.banner = "Dochi's FTP Server."
 
    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 65535)
    
    address = (FTP_HOST, FTP_PORT)
    server = FTPServer(address, handler)
    
    server.max_cons = 256
    server.max_cons_per_ip = 5
 
    server.serve_forever()
 
if __name__ == '__main__':
    main()