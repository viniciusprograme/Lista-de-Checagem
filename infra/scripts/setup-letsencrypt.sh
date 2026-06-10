#!/bin/sh
# Example script to obtain certs using certbot (needs docker or system installation)
DOMAIN=$1
EMAIL=$2
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "Usage: $0 example.com admin@example.com"
  exit 1
fi

# Using certbot on host (recommended) - ensure nginx is stopped or serves challenge
sudo apt-get update && sudo apt-get install -y certbot
sudo certbot certonly --standalone -d $DOMAIN --agree-tos --email $EMAIL --non-interactive

# Copy certs to infra/nginx/certs or mount in production
# Example path: /etc/letsencrypt/live/$DOMAIN

