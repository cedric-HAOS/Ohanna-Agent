from abc import ABC

from observer import ObservationExporter


def test_observation_exporter_is_abstract_contract() -> None:
    assert issubclass(ObservationExporter, ABC)
    assert ObservationExporter.__abstractmethods__ == {"export"}