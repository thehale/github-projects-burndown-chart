import os

# File I/O inspired by https://stackoverflow.com/a/4060259/14765128
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)))

with open(os.path.join(__location__, 'RepositoryProject.graphql')) as query:
    RepositoryProject = query.read()

with open(os.path.join(__location__, 'OrganizationProject.graphql')) as query:
    OrganizationProject = query.read()
