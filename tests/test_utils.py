"""
Randori Code Challenge utils tests module.
"""

from typing import Any

import pytest

from code_challenge.utils import duplicate, hashing, malicious


@pytest.fixture(scope="class")
def clean_duplicate_cache():
    """This fixture cleans the duplicate cache."""

    # yield to run the test
    yield

    # clear the cache after all the set of parametrized tests have finished
    duplicate._cache.clear()


class TestDuplicatePersistRequestHash:
    """This class is needed so that we can run the cleanup fixture after every set of parametrized tests."""

    @pytest.mark.parametrize(
        "client_host, request_hash",
        [
            ("host_1", "abc1"),
            ("host_2", "abc2"),
            ("host_3", "abc3"),
            ("host_3", "abc3"),
            ("host_3", "abc4"),
        ],
    )
    def test_persist_request_hash(self, client_host: str, request_hash: str, clean_duplicate_cache):
        """Test the persist_request_hash utility method."""

        duplicate.persist_request_hash(client_host=client_host, request_hash=request_hash)
        assert duplicate._cache.get(client_host) == request_hash


class TestDuplicateIsDuplicate:
    """This class is needed so that we can run the cleanup fixture after every set of parametrized tests."""

    @pytest.mark.parametrize(
        "client_host, request_hash, expected_is_duplicate",
        [
            # standard request
            ("host_1", "abc1", False),
            # standard request
            ("host_2", "abc2", False),
            # standard request
            ("host_3", "abc3", False),
            # duplicate request
            ("host_3", "abc3", True),
            # same host, different request
            ("host_3", "abc4", False),
        ],
    )
    def test_is_duplicate(
        self, client_host: str, request_hash: str, expected_is_duplicate: bool, clean_duplicate_cache
    ):
        """Test the is_duplicate utility method."""

        is_duplicate = duplicate.is_duplicate(client_host=client_host, request_hash=request_hash)
        assert is_duplicate == expected_is_duplicate

        # add the cache entry to the cache
        duplicate.persist_request_hash(client_host=client_host, request_hash=request_hash)


@pytest.mark.parametrize(
    "obj, expected_hash",
    [
        (12345, "827ccb0eea8a706c4c34a16891f84e7b"),
        ("abcdef", "e80b5017098950fc58aad83c8c14978e"),
        (TestDuplicateIsDuplicate, "31ca9b807a5d826ab27d62e7a47ea727"),
    ],
)
def test_hash_object(obj: Any, expected_hash: str):
    """Test the hash_object utility method."""

    hash_str = hashing.hash_object(obj=obj)
    assert hash_str == expected_hash


@pytest.mark.parametrize(
    "payload, expected_is_malicious",
    [
        # is_malicious must be a bool set to True to be malicious
        ({"is_malicious": "True"}, False),
        # typo
        ({"is_maliciouz": True}, False),
        # false
        ({"is_malicious": False}, False),
        # true
        ({"is_malicious": True}, True),
    ],
)
def test_is_malicious(payload: dict, expected_is_malicious: bool):
    """Test the is_malicious utility method."""

    is_malicious = malicious.is_malicious(payload=payload)
    assert is_malicious == expected_is_malicious
