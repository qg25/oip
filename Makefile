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
	${WINS_PYTHON} -m pip install opencv-python==3.4.6.27
	${WINS_PYTHON} -m pip install tensorflow
else
	${PYTHON} -m pip install --upgrade pip
	./requirements.sh
	${PYTHON} -m pip install opencv-python==3.4.6.27
	${PYTHON} -m pip install tensorflow
endif

	
# run:
# ifdef OS
# 	${WINS_PYTHON} src\mainGUI.py
# else
# 	${PYTHON} src/mainGUI.py
# endif


clean:
ifdef OS
	rmdir /S /Q src\__pycache__ src\tmp ${VENV_NAME}
else
	rm -rf src/__pycache__ src/tmp ${VENV_NAME}
endif