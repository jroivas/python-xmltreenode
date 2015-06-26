
all:
	@echo "***"
	@echo "*** Run \"make unittests\" to run all unit tests"
	@echo "*** Run \"make coversa\" to run coverage"
	@echo "***"

test: unittests

tests: unittests

unittests:
	@./test/runtests.sh

doc: referencedoc

referencedoc: xmltreenode_reference_manual_pdf

coverage: coverage_test coverage_report

coverage_test:
	coverage run ./test/testrunner.py

coverage_report:
	coverage report -m

clean:
	find -name "*.pyc" | xargs rm -f

flake8:
	flake8 --max-complexity 15 --ignore=E501 . | tee flake8.log

.PHONY: test tests unittests coverage coverage_test coverage_report clean flake8 all testpackage
