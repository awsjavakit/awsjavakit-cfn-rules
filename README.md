# Some custom Cloud Formation rules

### Run the rules on sample template files:

    1. make .venv
    2. make local-install (installs the module in the .venv)
    3. make cfn-lint (runs cfn-lint from the .venv)

Currently there is only one rule (tags_rule) that runs on a sample template file.