import nox


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the tests.
    """
    session.install("pandas")
    session.install(".[test]")
    session.run("pytest", *session.posargs)
