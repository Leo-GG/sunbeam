import os
import pytest
import shutil
import subprocess as sp
import sys
from pathlib import Path
from . import init

test_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(test_dir))
from config_fixture import output_dir, config

data_dir = Path(__file__).parent / "data"


@pytest.fixture
def setup(init):
    output_dir = init

    yield output_dir

    shutil.rmtree(output_dir / "sunbeam_output")


def test_sample_intake(init):
    output_dir = init
    sunbeam_output_dir = output_dir / "sunbeam_output"
    r1 = sunbeam_output_dir / "qc" / "00_samples" / "TEST_1.fastq.gz"
    r2 = sunbeam_output_dir / "qc" / "00_samples" / "TEST_2.fastq.gz"

    sp.check_output(
        [
            "sunbeam",
            "run",
            "--profile",
            f"{output_dir}",
            "--notemp",
            f"{r1}",
            f"{r2}",
        ]
    )

    assert os.path.islink(r1)
    assert os.path.islink(r2)