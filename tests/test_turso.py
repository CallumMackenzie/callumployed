from callumployed.data import db


def test_turso_vector_functions_are_available() -> None:
    connection = db.connect(":memory:")

    row = connection.execute(
        "SELECT vector_extract(vector32('[0.1, 0.2]')) AS embedding"
    ).fetchone()

    assert row is not None
    assert dict(row) == {"embedding": "[0.1,0.2]"}
