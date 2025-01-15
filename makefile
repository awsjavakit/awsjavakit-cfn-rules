
.PHONY: setup update wheel poetry-export local-install test

.venv:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install pipx && deactivate
	. .venv/bin/activate && python -m pip install poetry==1.8.5 && deactivate
	. .venv/bin/activate && pip install pytest-cov pytest-xdist && deactivate
	. .venv/bin/activate &&  poetry install && deactivate
	. .venv/bin/activate && pip install poetry-plugin-export && deactivate

poetry-update: .venv
	. .venv/bin/activate && poetry update && deactivate

poetry-export: .venv
	rm -rf dist
	. .venv/bin/activate && poetry build && deactivate
	. .venv/bin/activate && poetry export -f requirements.txt --output requirements.txt && deactivate

local-install: poetry-export
	. .venv/bin/activate && python -m pip install --force-reinstall dist/awsjavakit_cfn_rules-0.0.2-py3-none-any.whl && deactivate

test: .venv
	. .venv/bin/activate && poetry run pytest && deactivate

clean:
	rm -rf dist
	rm -rf .venv
	rm -rf poetry.lock

publish: poetry-export
	. .venv/bin/activate && python -m pip install build twine && deactivate
	. .venv/bin/activate && python -m twine upload -r testpypi -u __token__ -p ${PYPI_TOKEN} dist/* && deactivate

cfn-lint:
	. .venv/bin/activate && cfn-lint && deactivate

