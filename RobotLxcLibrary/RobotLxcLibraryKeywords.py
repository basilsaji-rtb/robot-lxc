#!/usr/bin/python

import lxc
from robot.api import logger
from robot.utils import asserts
import paramiko
import time
from scp import SCPClient

_container_dict = dict()

class RobotLxcLibraryKeywords(object):

    def __init__(self):
        self._container_ = None
        self._prompt_ = None
        self._ssh_ = None
        self._chan_ = None
        pass

    def container_ssh_channel_build(self, name):
        global _container_dict
        cdict = _container_dict[name]
        _ssh_ = paramiko.SSHClient()
        _ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_.connect(cdict["ip"],username="ubuntu", password="ubuntu")
        _chan_ = _ssh_.invoke_shell()
        _chan_.send("sudo su -\n"+"ubuntu\n")
        time.sleep(1)
        _chan_.send("PS1='~##~ '\nls\n")
        time.sleep(1)
        buff = ''
        while not buff.endswith("~##~ "):
            resp = _chan_.recv(1024)
            buff += resp
            print buff
        print buff
        cdict["ssh"] = _ssh_
        cdict["channel"] = _chan_
        _container_dict[name] = cdict

    def container_cache(self, name):
        global _container_dict
        _container_ = lxc.Container(name)
        cdict = dict()
        cdict["container"] = _container_
        cdict["name"] = name
        cdict["ip"] = str(_container_.get_ips(timeout=10)[0])
        _ssh_ = paramiko.SSHClient()
        _ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_.connect(cdict["ip"],username="ubuntu", password="ubuntu")
        _chan_ = _ssh_.invoke_shell()
        _chan_.send("sudo su -\n"+"ubuntu\n")
        time.sleep(1)
        _chan_.send("PS1='~##~ '\nls\n")
        time.sleep(1)
        buff = ''
        while not buff.endswith("~##~ "):
            resp = _chan_.recv(1024)
            buff += resp
            print buff
        print buff
        cdict["ssh"] = _ssh_
        cdict["channel"] = _chan_
        _container_dict[name] = cdict
        logger.info("LXC container cached: name - {}".format(name)) 

    def container_create(self, name, template="ubuntu", rel="trusty", arch="amd64"):
        global _container_dict
        _container_ = lxc.Container(name)
        _container_.create(template)
#        _container_.create(template, {"release": rel, "architecture": arch})
        cdict = dict()
        cdict["container"] = _container_
        cdict["name"] = name
        cdict["template"] = template
        cdict["ip"] = None
        cdict["ssh"] = None
        cdict["channel"] = None
        _container_dict[name] = cdict
        logger.info("LXC container created: name - {} template - {}".format(name, template)) 

    def container_wait(self, name, state):
        global _container_dict
        _container_ = _container_dict[name]["container"]
        _container_.wait(state, 30)

    def container_stop(self, name):
        global _container_dict
        _container_ = _container_dict[name]["container"]
        _container_.shutdown()
        _container_.stop()
        _container_.wait("STOPPED", 10)
        logger.info("LXC container stopped: name - {}".format(name)) 

    def container_start(self, name):
        global _container_dict
        _container_ = _container_dict[name]["container"]
        cdict = _container_dict[name]
        logger.info(str(cdict))
        _container_.start()
        _container_.wait("RUNNING", 5)
        logger.info("LXC container started: name - {}".format(name)) 
        cdict["ip"] = str(_container_.get_ips(timeout=10)[0])
        _ssh_ = paramiko.SSHClient()
        _ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_.connect(cdict["ip"],username="ubuntu", password="ubuntu")
        _chan_ = _ssh_.invoke_shell()
        _chan_.send("sudo su -\n"+"ubuntu\n")
        time.sleep(1)
        _chan_.send("PS1='~##~ '\nls\n")
        time.sleep(1)
        buff = ''
        while not buff.endswith("~##~ "):
            resp = _chan_.recv(1024)
            buff += resp
            print buff
        print buff
        cdict["ssh"] = _ssh_
        cdict["channel"] = _chan_
        _container_dict[name] = cdict

    def container_get_ip(self, name):
        global _container_dict
        cont = _container_dict[name]
        ip = cont["ip"]
        return ip

    def container_execute_cmd(self, name, cmd):
        global _container_dict
        _container_ = _container_dict[name]["container"]
        cmdlist = cmd.split(" ")
        _container_.attach_wait(lxc.attach_run_command, cmdlist)

    def container_destroy(self, name):
        global _container_dict
        _container_ = _container_dict[name]["container"]
        _container_.shutdown(timeout=10)
        _container_.stop()
        _container_.wait("STOPPED", 10)
        _container_.destroy()
        logger.info("LXC container destroyed")

    def container_execute_as_root(self, name, cmd):
        global _container_dict
        _container_ = _container_dict[name]
        try:
            _container_["channel"].send(cmd + "\n")
        except:
            self.container_ssh_channel_build(name)
            _container_ = _container_dict[name]
            _container_["channel"].send(cmd + "\n")
        buff = ''
        while not buff.endswith("~##~ "):
            resp = _container_["channel"].recv(1024)
            buff += resp
        return buff

    def container_put_file(self, name, filename, location):
        global _container_dict
        _container_ = _container_dict[name]
        scp = SCPClient(_container_["ssh"].get_transport())
        scp.put(filename, location)
        scp.close()
