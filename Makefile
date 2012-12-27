all: sdist

build:
	python setup.py build
sdist:
	python setup.py sdist
test:
	python setup.py test
install:
	python setup.py install
clean:
	python setup.py clean --all
	rm scratch/*.pyc
	rm tests/*.pyc
