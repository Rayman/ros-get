import pytest
from ros_get.__main__ import parse_args


def test_parse_no_command(capsys):
    """It should print an error message when no command is provided"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        parse_args([])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0

    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'the following arguments are required' in captured.err or 'too few arguments' in captured.err


def test_parse_status():
    func, args = parse_args(['status'])
    assert func == 'status'
    assert not args.verbose


def test_parse_status_verbose():
    func, args = parse_args(['--verbose', 'status'])
    assert func == 'status'
    assert args.verbose
