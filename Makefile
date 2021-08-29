VENV_NAME=env
PYTHON=${VENV_NAME}/bin/python
WINS_PYTHON=${VENV_NAME}/Scripts/python
PIP=${VENV_NAME}/Scripts/pip

.PHONY: create install run clean rpi-create rpi-install rpi-run rpi-clean
.DEFAULT: create


create: setup.py
ifdef OS
	python setup.py create
else
	python3 setup.py create
	sudo apt-get install libopenblas-dev -y
	
endif
	make install
	

install:
ifdef OS
	${WINS_PYTHON} -m pip install --upgrade pip
	${WINS_PYTHON} -m pip install -r requirements.txt
	${WINS_PYTHON} -m pip install -r wins-requirements.txt
else
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt
	${PYTHON} -m pip install -r rpi-requirements.txt
	${PYTHON} -m pip install --index-url https://google-coral.github.io/py-repo/ tflite_runtime
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
	sudo apt-get remove --auto-remove libopenblas-dev -y
endif




rpi-create:
ifdef OS
	make create
else
	python3 -m pip install --upgrade pip
	sudo apt-get install libopenblas-dev -y
	make rpi-install
endif


rpi-install:
ifdef OS
	make install
else
	sudo python3 -m pip install -r requirements.txt
	sudo python3 -m pip install -r rpi-requirements.txt
	chmod +x src/rpi/mainGUI.py
endif


rpi-run:
ifdef OS
	make run
else
	python3 src/rpi/mainGUI.py
endif


rpi-clean:
ifdef OS
	make clean
else
	python3 setup.py clean
	sudo python3 -m pip uninstall -r requirements.txt -y
	sudo python3 -m pip uninstall -r rpi-requirements.txt -y
	sudo apt-get remove --auto-remove libopenblas-dev -y
endif

