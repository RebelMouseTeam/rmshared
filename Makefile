OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

export PYTHONPATH:=${PWD}

lint:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@uv run flake8 --exclude=tests,.venv --max-line-length=160 --ignore=F541,E741 .

test: clean lint
	@echo "$(OK_COLOR)==> Running tests ...$(NO_COLOR)"
	@uv run pytest -vvv --cache-clear

tag:
	@if [ -z "$(VERSION)" ]; then echo "Usage: make tag VERSION=x.y.z"; exit 1; fi
	@echo "$(OK_COLOR)==> Creating tag $(VERSION) ...$(NO_COLOR)"
	@git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	@echo "$(OK_COLOR)==> Pushing tag $(VERSION) to origin ...$(NO_COLOR)"
	@git push origin "v$(VERSION)"

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

build:
	@echo "$(OK_COLOR)==> Building package ...$(NO_COLOR)"
	@uv build

install:
	@echo "$(OK_COLOR)==> Installing dependencies ...$(NO_COLOR)"
	@uv sync --extra dev
