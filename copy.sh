#!/bin/bash
dest=/var/www/html/cgistore
mkdir -p ${dest}
cp -a *.py ${dest}
cp -R pages css data html js utils ${dest}
find ${dest} -type f -name "*\.py" | xargs chmod 755
chmod 755 -R "${dest}/pages" "${dest}/css" "${dest}/data" "${dest}/html" "${dest}/js" "${dest}/utils"
cd ${dest}
cd ..
#python -m cgistore.utils.helpers
#python -m cgistore.data.dao