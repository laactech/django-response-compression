# Contributing to django-require-login
To submit new code to the project you'll need to:

1. Fork the repo
2. Clone your fork on your local computer:
`git clone https://github.com/<username>/django-require-login.git`
3. Install [poetry](https://github.com/sdispater/poetry#installation) for managing
dependencies
4. Install django-require-login locally: `poetry install`
5. Run the test suite: `pytest`
6. Install the linters: `pre-commit install`
7. Create a branch off of `master` for your work: 
    * `git checkout master`
    * `git checkout -b <branch-name>`
8. Make your changes
9. Add any tests or documentation necessary
10. Push to your remote: `git push origin <branch-name>`
11. [Open a pull request](https://github.com/laactech/django-response-compression/pulls)