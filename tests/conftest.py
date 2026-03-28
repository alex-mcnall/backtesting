import sys
import pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src/currency_converter"))

from instrument import Instrument

@pytest.fixture
def sample_instrument():
    return Instrument("Advanced Micro Devices", "AMD")
