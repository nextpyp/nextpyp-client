

from testlib import MockTransport


def test_version() -> None:
    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        'version': '1.2.3',
        'apiVersion': '4.5.6'
    }
    versions = client.services.apps.versions()
    assert versions.version == '1.2.3'
    assert versions.api_version == '4.5.6'


def test_is_compatible() -> None:

    transport = MockTransport()
    client = transport.client()

    def check(local: str, remote: str) -> bool:
        client.api_version = local
        transport.next_response = {
            'version': '1.2.3',
            'apiVersion': remote
        }
        return client.is_compatible()

    # exact same version should be fine
    assert check('1.2.3', '1.2.3') is True

    # patch change is ok
    assert check('1.2.3', '1.2.4') is True
    assert check('1.2.3', '1.2.24') is True
    assert check('1.2.3', '1.2.2') is True
    assert check('1.2.3', '1.2.0') is True

    # minor change is ok
    assert check('1.2.3', '1.3.0') is True
    assert check('1.2.3', '1.3.3') is True
    assert check('1.2.3', '1.3.4') is True
    assert check('1.2.3', '1.4.0') is True
    assert check('1.2.3', '1.44.0') is True
    assert check('1.2.3', '1.1.0') is True
    assert check('1.2.3', '1.0.0') is True

    # major change is not
    assert check('1.2.3', '0.0.0') is False
    assert check('1.2.3', '0.2.3') is False
    assert check('1.2.3', '2.0.0') is False
    assert check('1.2.3', '2.2.3') is False
