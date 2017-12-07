#!/usr/bin/env python
import subprocess


def test():
    ret1, ret2 = subprocess.getstatusoutput("ssh -i /root/.ssh/id_rsa ipfs 'ipfs add /export/img/1.jpg && rm -rf /export/img/1.jpg'")
    data = ret2.split(' ')
    print(data[1])

if __name__ == '__main__':
    test()
