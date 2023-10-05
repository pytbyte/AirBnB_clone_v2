#!/usr/bin/env bash
# Check if Nginx is installed, and if not, install it
install_nginx() {
    if ! command -v nginx &> /dev/null; then
        sudo apt update
        sudo apt install nginx -y
    fi
}

# Function to create the necessary directories
create_directories() {
    sudo mkdir -p "/data/web_static/releases/test/"
    sudo mkdir -p "/data/web_static/shared/"
}

# Function to create a fake HTML file for testing
create_fake_html() {
    body_content="We are live!"
    html_content="<html>
      <head></head>
      <body>$body_content</body>
    </html>"

    echo "$html_content" | sudo tee /data/web_static/releases/test/index.html > /dev/null
}


# Function to remove existing symbolic link and create a new one
create_symbolic_link() {
    rm -rf /data/web_static/current
    ln -s /data/web_static/releases/test/ /data/web_static/current
}

# Function to set ownership of /data/ recursively to the ubuntu user and group
set_ownership() {
    sudo chown -R ubuntu:ubuntu /data/
}

# Function to update the Nginx configuration
update_nginx_config() {
    config="/etc/nginx/sites-available/default"
    sudo wget -q -O "$config" http://exampleconfig.com/static/raw/nginx/ubuntu20.04/etc/nginx/sites-available/default
    echo 'Hello World!' | sudo tee /var/www/html/index.html > /dev/null
    sudo sed -i '/^}$/i \ \n\tlocation \/redirect_me {return 301 https:\/\/www.youtube.com\/watch?v=QH2-TGUlwu4;}' $config
    sudo sed -i '/^}$/i \ \n\tlocation @404 {return 404 "Ceci n'\''est pas une page\\n";}' $config
    sudo sed -i 's/=404/@404/g' $config
    sudo sed -i "/^server {/a \ \tadd_header X-Served-By $HOSTNAME;" $config
    sudo sed -i '/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/;index index.html;}' $config
}

# Function to restart Nginx
restart_nginx() {
    sudo service nginx restart
}

# Main script execution
trap 'exit 0' ERR

install_nginx
create_directories
create_fake_html
create_symbolic_link
set_ownership
update_nginx_config
restart_nginx

exit 0
