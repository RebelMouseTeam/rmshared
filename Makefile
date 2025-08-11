OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

export PYTHONPATH:=${PWD}
version=`python -c 'import rmshared; print(rmshared.__version__)'`
filename=rmshared-`python -c 'import rmshared; print(rmshared..__version__)'`.tar.gz

lint:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@flake8 --exclude=tests --max-line-length=160 --ignore=F541,E741 .

test: clean lint
	@echo "$(OK_COLOR)==> Running tests ...$(NO_COLOR)"
	@py.test -vvv --cache-clear

tag:
	@echo "$(OK_COLOR)==> Creating tag $(version) ...$(NO_COLOR)"
	@git tag -a "v$(version)" -m "Version $(version)"
	@echo "$(OK_COLOR)==> Pushing tag $(version) to origin ...$(NO_COLOR)"
	@git push origin "v$(version)"

bump:
	@bumpversion --commit --current-version $(version) patch rmshared/__init__.py --allow-dirty

bump-minor:
	@bumpversion --commit --current-version $(version) minor rmshared/__init__.py --allow-dirty

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

publish:
	@echo "$(OK_COLOR)==> Releasing package ...$(NO_COLOR)"
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@rm -fr build dist .egg pook.egg-info

install-dependencies:
	@echo "$(OK_COLOR)==> Installing development dependencies ...$(NO_COLOR)"
	@pip install -e .[dev]
