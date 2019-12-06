#!/bin/sh

set -e

# Usage:
#    /entrypoint.sh web
#    /entrypoint.sh server
#    /entrypoint.sh any-command

run_web() {
    # https://github.com/jwilder/nginx-proxy/blob/master/docker-entrypoint.sh#L22
    local RESOLVERS=$(awk '$1 == "nameserver" {print ($2 ~ ":")? "["$2"]": $2}' ORS=' ' /etc/resolv.conf | sed 's/ *$//g')
    sed -i "s@{{RESOLVERS}}@${RESOLVERS}@g" /etc/nginx/conf.d/default.conf
    sed -i "s@{{WEB_PORT}}@${WEB_PORT:-80}@g;s@{{SERVER_URL}}@${SERVER_URL:-localhost:8080}@g" /etc/nginx/conf.d/default.conf

    exec nginx -g "daemon off;"
}

run_server() {
    python3 manage.py migrate
    exec gunicorn \
        --bind=0.0.0.0:${SERVER_PORT:-8080} \
        --workers=4 \
        --name="CMS Server" \
        natureself.wsgi
}

help() {
    echo "Usage:"
    echo "    docker run ... web         # start frontend (and http entrypoint)"
    echo "    docker run ... server      # start server"
    echo "    docker run ... any-command # run specified command in the container"
}

if test -z "$1"; then
    help
    exit 1
fi

case "$1" in
    web)
        run_web
        ;;
    server)
        run_server
        ;;
    *)
        exec "$@"
        ;;
esac
