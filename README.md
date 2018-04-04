# phocode

## Requirements
- `python3.5.2`
- `pip3`
- `virtualenv` installed using `pip3 intall virtualenv`

## Set Up

1. Change directory into the root directory.
```
cd phocode
```

- Create a Python virtual environment.
```
python -m venv env        # assuming python 3.5.2 is the default
```

- Switch to Python virtual environment
```
. env/bin/activate        # for unix
```

- Upgrade packaging tools.
```
pip install --upgrade pip setuptools
```

- Install required package from pip
```
pip install -r requirements.txt
```

- Install the project in editable mode with its testing requirements.
```
pip install -e ".[testing]"
```

## Running Project

- Run project's tests.
```
pytest                    # optional
```

- Run in development.
```
pserve development.ini    # available through port 6543
```

- Run in production.
```
pserve production.ini    # available through port 6543
```
