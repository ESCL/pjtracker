base:
  '*':
    - core.swap
    - core.python
    - services.nginx

    # Temp until we sort out uwsgi
    - app.environment
    # - services.uwsgi