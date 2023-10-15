import socket

def get_constants (prefix):

    return {
        getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)
    }
families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

for response in socket.getaddrinfo('www.kyungnam.ac.kr', 'http'):

    family, socktype, proto, canoname, sockaddr = response

    print('Family        :', families[family])
    print('type          :', types[socktype])
    print('Protocol      :', protocols[proto])
    print('Canonical name:', canoname)
    print('Socket address:', sockaddr)
