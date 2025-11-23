from examples.garden_of_thoughts import run_garden  # type: ignore


def test_garden_runs_and_returns_entropy():
    result = run_garden(steps=10, seed=1, verbose=False)
    assert 0.0 <= result["final_entropy"] <= 1.0
    assert result["ticks"] == 10
