#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/hanlon_project/:/home/ubuntu/hanlon_project/hanlon_env/bin/
{ python source.py & cat /home/ubuntu/hanlon_project/mail_meta.txt; } | sendmail apoorvchandrakar@gmail.com