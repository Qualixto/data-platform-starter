import pytest

from data_platform_starter.core import greet


@pytest.mark.parametrize(
    ("name", "expected"),
    [("Ada", "Hello, Ada!"), ("  Ada  ", "Hello, Ada!"), ("", "Hello, world!")],
)
def test_greet(name: str, expected: str) -> None:
    assert greet(name) == expected


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    from data_platform_starter.__main__ import main

    main(["Ada"])

    assert capsys.readouterr().out == "Hello, Ada!\n"
