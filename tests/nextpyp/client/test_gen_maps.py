from nextpyp.client.gen import TwoDClassData


def test_map_round_trip():
    """Kotlin maps with string keys travel as JSON objects, both ways."""
    json = {'classNum': 1, 'numParticles': 10, 'metadata': {'resolution': 8.5, 'score': 0.5}, 'classScore': None}
    data = TwoDClassData.from_json(json)
    assert data.metadata == {'resolution': 8.5, 'score': 0.5}
    assert data.to_json()['metadata'] == {'resolution': 8.5, 'score': 0.5}
