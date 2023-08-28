from ..conf import BASE_PATH

FROM_TEMPLATE = """\
FROM $image:$tag $name

LABEL maintainer="Zack Hankin <docker@hankin.io>"
"""

LOCALE_FIX = """
# ==================
# Fix certificate and LOCALE problem
# ==================

RUN apt-get update \\
    && apt-get install -y --no-install-recommends locales \\
    && rm -rf /var/lib/apt/lists/* \\
    && dpkg-reconfigure locales \\
    && echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen \\
    && locale-gen en_US.UTF-8 \\
    && update-locale LANG=en_US.UTF-8

ENV LC_ALL=en_US.UTF-8 \\
    LANG=en_US.UTF-8 \\
    LANGUAGE=en_US.UTF-8

"""

ENDING = f"""

RUN chmod ug+x /docker-entrypoint.sh \\
    && chown root:www-data /docker-entrypoint.sh \\
    && chmod -R ug+x /docker-entrypoint.d \\
    && chown -R root:www-data /docker-entrypoint.d

COPY *.html /usr/share/nginx/html/
    
USER root

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
"""