from pytest import fixture  # type:ignore


class SimplestContextManager:
    def __enter__(self):
        pass

    def __exit__(self, exc, exc_type, tb):
        # no need to re-reaise `exc`.
        #
        # SEE: https://docs.python.org/3/reference/datamodel.html#object.__exit__
        #
        # > Note that __exit__() methods should not reraise the passed-in exception;
        # > this is the caller’s responsibility.
        #
        pass


@fixture
def simplest_ctxman():
    return SimplestContextManager()
