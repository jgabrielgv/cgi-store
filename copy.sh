#!/bin/bash
dest=/var/www/html/cgistore
cp -a *.py ${dest}
cp -a *.html ${dest}
cp -R css ${dest}
cp -R data ${dest}
cp -R js ${dest}
cp -R utils ${dest}
find ${dest} -type f -name "*\.py" | xargs chmod 755
find ${dest} -type f -name "*\.html" | xargs chmod 444
chmod 755 -R "${dest}/css"
chmod 755 -R "${dest}/data"
chmod 755 -R "${dest}/js"
chmod 755 -R "${dest}/utils"