from pytest import fixture, raises  # type:ignore


def test_simplest_context_manager_ok(simplest_ctxman):
    with simplest_ctxman:
        pass
        

def test_simplest_context_manager_with_exception(simplest_ctxman):
    with raises(Exception):
        with simplest_ctxman:
            raise Exception("Here's Johnny!")
    
