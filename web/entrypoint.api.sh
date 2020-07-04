#!/usr/bin/env sh

gunicorn web.wsgi_app:application --bind 0.0.0.0:9000

exec "$@"