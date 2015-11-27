# Install python2, python3 and pip

python2:
  pkg.installed:
    - pkgs:
      - python
      - python-dev

python3:
  pkg.installed: []

pip:
  pkg.installed:
    - name: python-pip
    - require:
      - pkg: python2

pip3:
  pkg.installed:
    - name: python3-pip
    - require: python3

pip-update:
  cmd.run:
    - name: pip install -U pip
    - require:
      - pkg: pip
