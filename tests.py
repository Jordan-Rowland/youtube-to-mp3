from yt_to_mp3 import *
import pytest


def test_safe_name():
    assert safe_name("test () **!") == "test () "
    assert safe_name(
        "Elliott Smith #- Ballad Of Big Nothing &(Official)"
    ) == "Elliott Smith - Ballad Of Big Nothing (Official)"


