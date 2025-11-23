from elysia_engine.cymatics import frequency_to_pattern
from examples.cymatics_ascii import render_pattern  # type: ignore


def test_render_pattern_outputs_grid():
    pattern = frequency_to_pattern(40.0, phase=0.1)
    art = render_pattern(pattern, width=30, height=15)
    assert isinstance(art, str)
    assert "o" in art  # path markers


def test_render_pattern_gates_marked():
    pattern = frequency_to_pattern(80.0, phase=0.0)
    art = render_pattern(pattern, width=30, height=15)
    assert any(ch.isdigit() for ch in art)
