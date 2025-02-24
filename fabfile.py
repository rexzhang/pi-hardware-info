from fabric import task


@task
def build(c):
    c.run("pip install -U -r requirements-dev.txt")
    c.run("rm -rf dist/*")
    c.run("python -m build")


@task
def publish(c):
    c.run(
        "python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*"
    )
