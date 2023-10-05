#!/usr/bin/env bash
# Check if Nginx is installed, and if not, install it
# Function to install Nginx if not already installed
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

# Function to set ownership of /data/ recursively to the ubuntu user and group
set_ownership() {
    sudo chown -R ubuntu:ubuntu /data/
}

# Function to update the Nginx configuration
update_nginx_config() {
    config="/etc/nginx/sites-available/default"
    sudo wget -q -O "$config" http://exampleconfig.com/static/raw/nginx/ubuntu20.04/etc/nginx/sites-available/default
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
set_ownership
update_nginx_config
restart_nginx

exit 0
