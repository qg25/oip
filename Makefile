VENV_NAME=env
PYTHON=${VENV_NAME}/bin/python
WINS_PYTHON=${VENV_NAME}/Scripts/python
PIP=${VENV_NAME}/Scripts/pip

.PHONY: create install run clean
.DEFAULT: create

create: setup.py
ifdef OS
	python setup.py create
endif
	make install
	

install:
ifdef OS
	${WINS_PYTHON} -m pip install --upgrade pip
	${WINS_PYTHON} -m pip install -r requirements.txt
else
	python3 -m pip install --upgrade pip
	sudo python3 -m pip install -r requirements.txt
	chmod +x src/rpi/mainGUI.py
endif


run:
ifdef OS
	${WINS_PYTHON} src\rpi\mainGUI.py
else
	python3 src/rpi/mainGUI.py
endif


clean:
ifdef OS
	python setup.py clean
else
	python3 setup.py clean
	sudo python3 -m pip uninstall -r requirements.txt -y
endif