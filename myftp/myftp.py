#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ftplib import FTP


class MyFTP(object):
    def __init__(self, host, user, passwd):
        self.host = host
        self.username = user
        self.password = passwd
        self.ftp = FTP()
        self.login()

    def __del__(self):
        self.ftp.quit()

    def login(self):
        self.ftp.connect(self.host, 21)
        self.ftp.login(self.username, self.password)

    def uploadfile(self, remote_file, filename):
        with open(filename, 'rb') as fp:
            self.ftp.storbinary('STOR '+remote_file, fp, 1024)

    def downloadfile(self, remote_file, filename):
        with open(filename, 'wb') as fp:
            self.ftp.retrbinary('RETR '+remote_file, fp.write, 1024)

    def deletefile(self, remote_file):
        self.ftp.delete(remote_file)

    def createpath(self, remote_path):
        self.ftp.mkd(remote_path)


if __name__ == "__main__":
    ftp = MyFTP('127.0.0.1', 'user', 'password')
    ftp.createpath('send')
    filename = 'test.txt'
    ftp.uploadfile('send/'+filename, filename)

    ftp.downloadfile('send/'+filename, 'testr.txt')
    ftp.deletefile('send/'+filename)
