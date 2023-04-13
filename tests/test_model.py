"""Unit tests for measurement module"""

import pytest

from model.model import BodyMeasurement


@pytest.mark.parametrize(
    "model_complexity, enable_segmentation, min_detection_confidence",
    [
        (0, True, 0.9),
    ],
)
def test_bodymeasurement_init(
    model_complexity: int, enable_segmentation: bool, min_detection_confidence: float
) -> None:
    """Test class initilization"""
    bm_ = BodyMeasurement(model_complexity, enable_segmentation, min_detection_confidence)

    assert bm_.static_image_mode
    assert bm_.model_complexity == model_complexity
    assert bm_.enable_segmentation == enable_segmentation
    assert bm_.min_detection_confidence == min_detection_confidence
