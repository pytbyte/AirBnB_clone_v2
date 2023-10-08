# instal and configure nginx
exec {'update_system':
  command => '/usr/bin/apt-get update',
}
-> package { 'nginx':
  ensure => installed,
}
-> exec { 'task0':
  command => '/usr/bin/mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"',
}
-> exec { 'task1':
  command => '/usr/bin/echo "Hi!" | sudo tee /data/web_static/releases/test/index.html > /dev/null',
}
-> exec { 'task2':
  command => '/usr/bin/rm -rf /data/web_static/current',
}
-> exec { 'task3':
  command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
}
-> exec { 'task4':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}
-> exec { 'hbnb_static':
  command => 'sudo sed -i "/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/;index index.html;}" /etc/nginx/sites-enabled/default',
  provider => shell,
}
-> exec { 'task5':
  command => '/usr/sbin/service nginx restart',
}