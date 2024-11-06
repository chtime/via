#!/bin/sh

gunicorn \
	--access-logfile - \
	app:app
