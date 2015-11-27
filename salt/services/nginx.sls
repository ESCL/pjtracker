# Install and configure nginx web server

nginx-install:
  pkg.installed:
    - name: nginx

nginx-run:
  service.running:
    - require:
      - pkg: nginx-install
    - watch:
      - file: nginx-config

nginx-config:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://services/nginx.conf
