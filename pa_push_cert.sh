#!/bin/bash
script_path="/usr/local/sbin"
if [ -d /etc/letsencrypt/live ]; then
        cd /etc/letsencrypt/live
		for file in /etc/letsencrypt/live/*; do
				cd $file
				fn=`echo $file|cut -d \/ -f5`
				name=`hostname`
				python $script_path/pa_push_cert.py $name
				echo uploaded : $name
				rm le_export.pkcs12
		done
fi
else
        echo "Error: Lets Encrypt folder not found"
fi
