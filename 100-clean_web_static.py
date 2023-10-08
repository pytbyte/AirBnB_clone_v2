#!/usr/bin/python3
""" clean_web_static
"""
from fabric.api import task, local, env, put, run, runs_once
from datetime import datetime
import os


env.hosts = ["100.26.157.101", "54.157.150.183"]


@runs_once
def do_pack():
    """ do_pack
        zip for moving
        sudo fab -f 1-pack_web_static.py do_pack
    """
    date_data = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    z_path = "versions/web_static_{}.tgz".format(date_data)
    print("Packing web_static to {}".format(z_path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, z_path)).succeeded:
        return z_path
    return None


@task
def do_deploy(archive_path):
    """ method doc
        fab -f 2-do_deploy_web_static.py do_deploy:
        archive_path=versions/web_static_20231004201306.tgz
        -i ~/.ssh/id_rsa -u ubuntu
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dpath, fn_no_ext))
        run("mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("rm /tmp/{}".format(fn_with_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    """ deployer of archives
        sudo fab -f 1-pack_web_static.py do_pack
    """
    deploy_path = do_pack()
    if deploy_path is None:
        return False
    return do_deploy(deploy_path)


@runs_once
def remove_local(number):
    """ archive manager
        sudo fab -f 1-pack_web_static.py do_pack
    """
    local("ls -dt versions/* | tail -n +{} | sudo xargs rm -fr".format(number))


@task
def do_clean(number=0):
    """ managed archives
        sudo fab -f 1-pack_web_static.py do_pack
    """
    if int(number) == 0:
        number = 1
    number = int(number) + 1
    remove_local(number)
    rem_path = "/data/web_static/releases/*"
    run("ls -dt {} | tail -n +{} | sudo xargs rm -fr".format(rem_path, number))
