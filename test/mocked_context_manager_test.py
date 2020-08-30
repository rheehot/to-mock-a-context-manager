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
