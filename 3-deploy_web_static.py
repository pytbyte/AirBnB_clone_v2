#!/usr/bin/python3
""" Fabric script that generates a .tgz archive """
from fabric.decorators import task
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["100.26.157.101", "54.157.150.183"]


@task
def deploy():
    """ Fabric script that creates and distributes an archive """
    file_name = do_pack()
    if file_name is None:
        return False
    return do_deploy(file_name)


@task
def do_deploy(archive_path):
    """Fabric script that distributes an archive to web servers"""
    try:
        if not os.path.exists(archive_path):
            return False
        unsplitted = archive_path.split("/")[-1]
        ext_splitted = archive_path.split("/")[-1].split(".")[0]
        pth = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p " + pth + ext_splitted)
        run("tar -xzf /tmp/{} -C {}{}/".format(unsplitted, pth, ext_splitted))
        run("rm /tmp/{}".format(unsplitted))
        run("mv {1}{0}/web_static/* {1}{0}/".format(ext_splitted, pth))
        run("rm -rf {}{}/web_static".format(pth, ext_splitted))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(pth, ext_splitted))
        return True
    except Exception as e:
        print("An error occurred: {}".format(e))
        return False


@runs_once
def do_pack():

    """generates a .tgz archive from web_static"""
    date_data = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date_data)
    local("mkdir -p versions")
    if local("tar -cvzf {} web_static/".format(file_name)).succeeded:
        return file_name
    return None
