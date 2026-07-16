VENV = .venv

ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV)\Scripts\python.exe
    PIP = $(VENV)\Scripts\pip.exe
else
    PYTHON = $(VENV)/bin/python
    PIP = $(VENV)/bin/pip
endif

hello:
	echo "Hello World from make"

$(VENV):
	python -m venv $(VENV)

install_deps: $(VENV)
	$(PIP) install -r requirements.txt