from pytest import fixture, raises  # type:ignore


class SimplestContextManager:
    __slots__ = ['rec']

    def __init__(self):
        self.rec = []
    
    def __enter__(self):
        self.rec.append('ENTER')

    def __exit__(self, exc, exc_type, tb):
        self.rec.append('EXIT')


@fixture
def simplest_ctxman():
    return SimplestContextManager()


def test_simplest_context_manager_ok(simplest_ctxman):
    with simplest_ctxman:
        pass
        

def test_simplest_context_manager_with_exception(simplest_ctxman):
    with raises(Exception):
        with simplest_ctxman:
            raise Exception("Here's Johnny!")
    
