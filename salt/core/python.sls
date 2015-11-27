# Install python2, python3 and pip

python:
  pkg.installed: []

python3:
  pkg.installed: []

pip:
  pkg.installed:
    - name: python-pip
    - require:
      - pkg: python

pip-update:
  cmd.run:
    - name: pip install -U pip
    - require:
      - pkg: pip
