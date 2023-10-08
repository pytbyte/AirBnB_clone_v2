#!/usr/bin/python3
"""_1-pack_web_static_

     Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        Path to the created archive if successful, None otherwise.
"""
from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        Path to the created archive if successful, None otherwise.
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_" + timestamp + ".tgz"
        local("mkdir -p versions")
        local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None
