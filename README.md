# Burndown Chart for GitHub Projects
An easy to use [burndown chart](https://www.scrum.org/resources/scrum-glossary#:~:text=B-,burn-down%20chart,-%3A%C2%A0a%20chart%20which) generator for [GitHub Project Boards](https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards).

## Table of Contents
* [Features](#features)
* [Installation](#installation)
* [Assumptions](#assumptions)
* [Usage](#usage)
* [Contributing](#contributing)
* [About](#about)

## Features
* Create a **burndown chart for a GitHub Project Board**.
* Works for **private repositories**.
* Includes a **trend line** for the current sprint.
* Supports custom labels for **tracking points for issues**

## Assumptions
This tool, while flexible, makes the following assumptions about your project management workflow:
* You use one and only one [GitHub Project Board](https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards) for each of your [Sprints](https://scrumguides.org/scrum-guide.html#the-sprint)
* You use one and only one [GitHub Milestone](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones) for each of your [User Stories](https://www.scrum.org/resources/blog/user-story-or-stakeholder-story)
* You use one and only one [GitHub Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) for each of your [Sprint Backlog Items/Tasks](https://scrumguides.org/scrum-guide.html#sprint-backlog)
* Each of your GitHub Issues has a [label](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels) indicating how many [points](https://www.scrum.org/resources/scrum-glossary#:~:text=several%20ways%20such%20as-,user%20story%20points,-or%20task%20hours.%20Work) its corresponding task is worth.
    - Furthermore, all labels that indicate point values have the format `<prefix><int>`.
    - However, multiple labels indicating points on the same Issue are supported.
* A Sprint Backlog Task is considered [Done](https://www.scrum.org/resources/professional-scrum-developer-glossary#:~:text=D-,definition%20of%20done%3A,-a%20shared%20understanding) if its corresponding GitHub Issue is Closed.

## Installation
### 0. Clone this repository
```
git clone https://github.com/jhale1805/github-projects-burndown-chart.git
cd github-projects-burndown-chart
```
### 1. Create a virtual environment
```
python -m venv ./venv
```

### 2. Activate the virtual environment

*Linux/Mac OS*
```
source venv/bin/activate
```
*Windows (Powershell)*
```
.\venv\Scripts\activate
```
*Windows (Command Prompt)*
```
.\venv\Scripts\activate.bat
```

### 3. Install the dependencies
```
pip install -r requirements.txt
```

## Usage
### Configuration
1. Create a [Personal Access Token](https://github.com/settings/tokens) with the `repo` scope.
    - Do not share this token with anyone! It gives the bearer full control over all private repositories you have access to!
    - This is required to pull the Project Board data from GitHub's GraphQL API.
2. Make a copy of `src/github_projects_burndown_chart/config/secrets.json.dist` without the `.dist` ending.
    - This allows the `.gitignore` to exclude your `secrets.json` from being accidentally committed.
3. Fill out the `github_token` with your newly created Personal Access Token.
4. Make a copy of `src/github_projects_burndown_chart/config/config.json.dist` without the `.dist` ending.
    - This allows the `.gitignore` to exclude your `config.json` from being accidentally committed.
5. Fill out all the configuration settings
    - `repository_project_query.repo_owner`: The username of the owner of the repo.
        - For example, `jhale1805`
    - `repository_project_query.repo_name`: The name of the repo.
        - For example, `github-projects-burndown-chart`
    - `repository_project_query.project_number`: The id of the project for which you want to generate a burndown chart. This is found in the URL when looking at the project board on GitHub.
        - For example, `1` from [`https://github.com/jhale1805/github-projects-burndown-chart/projects/1`](https://github.com/jhale1805/github-projects-burndown-chart/projects/1)
    - `settings.sprint_start_date`: The first day of the sprint. Formatted as `YYYY-MM-DD`. 
        - Must be entered here since GitHub Project Boards don't have an assigned start/end date.
        - For example, `2021-10-08`
    - `settings.sprint_end_date`: The last day of the sprint. Formatted as `YYYY-MM-DD`.
        - Must be entered here since GitHub Project Boards don't have an assigned start/end date.
        - For example, `2021-10-22`
    - `settings.points_label`: The prefix for issue labels containing the point value of the issue. Removing this prefix must leave just an integer.
        - For example: `Points: ` (with the space)
### Generating the Chart
1. Run `make run` to generate the burndown chart.
    - This will pop up an interactive window containing the burndown chart, including a button for saving it as a picture.

## Contributing
Contributions are welcome via a [Pull Request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

*The Legal Part*

By submitting a contribution, you are agreeing that the full contents of your contribution will be subject to the license terms governing this repository, and you are affirming that you have the legal right to subject your contribution to these terms.

## About
This project was first created by Joseph Hale (@jhale1805) and Jacob Janes (@jgjanes) to facilitate their coursework in the BS Software Engineering degree program at Arizona State University.

We hope it will be especially useful to other students in computing-related fields.