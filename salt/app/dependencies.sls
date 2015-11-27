# Install dependencies required by the application

pgsql-install:
  pkg.installed:
    - refresh: True
    - pkgs:
      - postgresql
      - libpq-dev
