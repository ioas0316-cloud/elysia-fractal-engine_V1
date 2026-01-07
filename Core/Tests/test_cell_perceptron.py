from Core.Foundation.Abstractions.Cell import Cell


def test_cell_perceptron_output_and_learning():
    cell = Cell(id="test", dna={}, properties={})

    features = {"value_mass": 1.0, "threat": 0.0}

    # With zero weights/bias, initial output is 0
    y0 = cell.perceptron_output(features)
    assert abs(y0) < 1e-6

    # Teach the cell that this feature pattern is "good" (target = 1)
    error = cell.perceptron_learn(features, target=1.0)
    assert error > 0  # We were below the target

    # After learning, output should move closer to the target
    y1 = cell.perceptron_output(features)
    assert y1 > y0

