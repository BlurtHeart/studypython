# -*- coding:utf-8 -*-
"""
    main
    ~~~~~~~~~~~~~~~~~~~

    logger in situation of multiprocesses.

    :copyright: (c) 2017 by Blurt Heart.
    :license: BSD, see LICENSE for more details.
"""
import pickle
import logging
import logging.handlers
from logging import makeLogRecord
import SocketServer
import struct


class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    '''Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is 
    configured locally.
    '''
    def handle(self):
        '''
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the record in pickle format. Logs the record according
        to whatever policy is configured locally.
        '''
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen-len(chunk))

            obj = self.unPickle(chunk)
            record = makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, chunk):
        return pickle.loads(chunk)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather
        # than the one implied by the record
        name = self.server.logname or record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketServer(SocketServer.ThreadingTCPServer):
    '''
    Simple TCP socket-based logging receiver
    '''
    def __init__(self, host='localhost', port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
        handler=LogRecordStreamHandler, logname=None):
        SocketServer.ThreadingTCPServer.__init__(self, (host,port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = logname

    def server_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                    [], [],
                                    self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def main():
    logging.basicConfig(filename='main.log', mode='a',
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    tcpserver = LogRecordSocketServer(logname='main.log')
    print 'About to start log server...'
    tcpserver.server_until_stopped()


if __name__ == "__main__":
    main()
