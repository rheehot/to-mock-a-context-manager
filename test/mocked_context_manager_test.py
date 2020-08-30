from unittest.mock import Mock, call, ANY
from pytest import mark, raises  # type:ignore

def test_mocked_ctxman_ok():
    ctxman_mock = Mock()

    ctxman_mock.__enter__ = Mock()
    ctxman_mock.__exit__ = Mock()

    with ctxman_mock:
        pass

    # verify mock
    ctxman_mock.__enter__.assert_called_once()
    ctxman_mock.__exit__.assert_has_calls([
        call(None, None, None)
    ])


def test_mocked_ctxman_with_exception__wrong():
    ctxman_mock = Mock()

    ctxman_mock.__enter__ = Mock()
    ctxman_mock.__exit__ = Mock()

    # THIS IS SO WRONG: did eat up raised exception.
    with ctxman_mock:
        raise Exception("Here's Johnny!")

    # verify mock
    ctxman_mock.__enter__.assert_called_once()
    ctxman_mock.__exit__.assert_has_calls([
        # been passed an exception
        call(Exception, ANY, ANY)
    ])

    #
    assert ctxman_mock.__exit__()  # it returns True.


def test_mocked_ctxman_with_exception__fixed():
    def exit_fn(exc, exc_type, tb):
        if exc is not None:
            raise exc        
    
    ctxman_mock = Mock()

    ctxman_mock.__enter__ = Mock()
    ctxman_mock.__exit__ = Mock(side_effect=exit_fn)

    # NOW it's working as expected:
    with raises(Exception):
        with ctxman_mock:
            raise Exception("Here's Johnny!")

    # verify mock
    ctxman_mock.__enter__.assert_called_once()
    ctxman_mock.__exit__.assert_has_calls([
        call(Exception, ANY, ANY)
    ])


def test_mocked_ctxman_with_exception__correct():
    """SEE: https://www.python.org/dev/peps/pep-0343/

    IMPORTANT: if mgr.__exit__() returns a "true" value, the exception
    is "swallowed". That is, if it returns "true", execution continues
    at the next statement after the with-statement, even if an
    exception happened inside the with-statement. However, if the
    with-statement was left via a non-local goto (break, continue or
    return), this non-local return is resumed when mgr.__exit__()
    returns regardless of the return value. The motivation for this
    detail is to make it possible for mgr.__exit__() to swallow
    exceptions, without making it too easy (since the default return
    value, None, is false and this causes the exception to be
    re-raised). The main use case for swallowing exceptions is to make
    it possible to write the @contextmanager decorator so that a
    try/except block in a decorated generator behaves exactly as if
    the body of the generator were expanded in-line at the place of
    the with-statement.

    """
    ctxman_mock = Mock()

    ctxman_mock.__enter__ = Mock()
    ctxman_mock.__exit__ = Mock(return_value=None)

    # CORRECT:
    with raises(Exception):
        with ctxman_mock:
            raise Exception("Here's Johnny!")

    # verify mock
    ctxman_mock.__enter__.assert_called_once()
    ctxman_mock.__exit__.assert_has_calls([
        call(Exception, ANY, ANY)
    ])
    
