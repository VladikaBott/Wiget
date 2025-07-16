from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "amount": "100"},
        {"id": 2, "state": "PENDING", "amount": "200"},
        {"id": 3, "state": "EXECUTED", "amount": "300"},
        {"id": 4, "state": "CANCELED", "amount": "400"},
    ]
