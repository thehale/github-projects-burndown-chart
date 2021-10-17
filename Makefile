instructions:
	@echo "[NOTE]: If you see any errors, make sure your virtual environment is active!"

build: instructions
	pip install -r requirements.txt


run: instructions
	cd ./src/github_projects_burndown_chart \
	&& PYTHONPATH=. python main.py $(project_type) $(project_name)

test: instructions
	coverage run \
		--source=src/github_projects_burndown_chart \
		--branch \
		-m unittest discover -v

.PHONY: build run test