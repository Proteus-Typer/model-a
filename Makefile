STL_FILES = base.stl hinged_lid.stl simple_lid.stl tandy_lid.stl

all: $(STL_FILES) lint

%.stl: %.py dimensions.py utils.py components/*py
	python $<

lint: .lint

.lint: *.py components/*.py
	flake8 
	black *.py */*.py
	touch .lint

