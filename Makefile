.PHONY: clean

all: clean vector

run: clean cython
	python changing_environment_ga.py -c quick_test.ini -o default_data

clean:
	-@rm -r *~ *.pyc *.csv *.c *.so fitness_function.cpp build default_data 2>/dev/null || true

test: cython
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage report -m

profile: cython
	-@rm -r profile_junk_data
	python profile.py

cython:
	python setup.py build_ext --inplace

multiprofile: cython
	-@rm -r multiprofile_junk_data
	python multiprofile.py

cleanprofile:
	-@rm -r profile_junk_data
	-@rm -r multiprofile_junk_data

submit: cython
	python qsub_generator.py