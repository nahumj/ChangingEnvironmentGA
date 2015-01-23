.PHONY: clean

all: clean vector

vector: 
	python changing_environment_ga.py -c vector_config.ini -o default_data

run:
	python changing_environment_ga.py -c config.ini -o default_data

clean:
	-@rm -r *~ *.pyc *.csv default_data 2>/dev/null || true

test:
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage report -m
