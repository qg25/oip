VENV_NAME=env
PYTHON=${VENV_NAME}/bin/python
WINS_PYTHON=${VENV_NAME}/Scripts/python
PIP=${VENV_NAME}/Scripts/pip

.PHONY: create install run clean
.DEFAULT: create

create: setup.py
ifdef OS
	python setup.py create
else
	python3 setup.py create
endif
	make install
	

install:
ifdef OS
	${WINS_PYTHON} -m pip install --upgrade pip
	${WINS_PYTHON} -m pip install pyserial
	${WINS_PYTHON} -m pip install guizero
else
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install pyserial
	${PYTHON} -m pip3 install guizero
	chmod +x src/rpi/mainGUI.py
endif


run:
ifdef OS
	${WINS_PYTHON} src\rpi\mainGUI.py
else
	${PYTHON} src/rpi/mainGUI.py
endif


clean:
ifdef OS
	python setup.py clean
else
	python3 setup.py clean
endif