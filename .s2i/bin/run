#!/bin/sh

gunicorn \
	--bind '0.0.0.0' \
	--access-logfile - \
	app:app
