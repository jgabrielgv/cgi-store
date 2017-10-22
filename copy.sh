#!/bin/bash
cp -a *.py /usr/lib/cgi-bin/
cp -a *.html /usr/lib/cgi-bin/
chmod 555 -R /usr/lib/cgi-bin/*.py
chmod 555 -R /usr/lib/cgi-bin/*.html
