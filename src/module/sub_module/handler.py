import sys
import os


class Handler(Tasks):

    _listen_port_life = ""

    def notify_host(self, host):
        if not self.is_host_notified(host):
            self.notified_hosts.append(host)
            return True
        return False

    def is_host_notified(self, host):
        return host in self.notified_hosts

    def serialize(self):
        result = super(Handler, self).serialize()
        result["is_handler"] = True
        return result
