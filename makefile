
.PHONY: setup update wheel poetry-export local-install

.venv:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install pipx && deactivate
	. .venv/bin/activate && python -m pip install poetry && deactivate
	. .venv/bin/activate && pip install pytest-cov pytest-xdist && deactivate
	. .venv/bin/activate &&  poetry install && deactivate
	. .venv/bin/activate && pip install poetry-plugin-export && deactivate

poetry-update: .venv
	. .venv/bin/activate && poetry update && deactivate

poetry-export: .venv
	. .venv/bin/activate && poetry build && deactivate
	. .venv/bin/activate && poetry export -f requirements.txt --output requirements.txt && deactivate

local-install: poetry-export
	. .venv/bin/activate && python -m pip install --force-reinstall dist/awsjavakit_cfn_rules-0.0.1-py3-none-any.whl && deactivate

clean:
	rm -rf dist
	rm -rf .venv

cfn-lint:
	. .venv/bin/activate && cfn-lint && deactivate
