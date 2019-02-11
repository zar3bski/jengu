# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3-onbuild

# COPY setting.py from build server to overwrite the default one (edit according to you emplacement) 
COPY /root/secrets/jengu/settings.py meds_pro/settings.py 

# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# ADD custom functions and trigger to the DB
ADD jengu/sql/jengu_base.sql /docker-entrypoint-initdb.d

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!