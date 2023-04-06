"""Unit tests for segmentation module"""

import pytest

from model.model import BodyMeasurement


@pytest.mark.parametrize(
    "model_complexity, enable_segmentation, min_detection_confidence",
    [(0, True, 0.9),],
)
def test_bodymeasurement_init(
    model_complexity: int, enable_segmentation: bool, min_detection_confidence: float
) -> None:
    """Test class initilization"""
    bm_ = BodyMeasurement(model_complexity, enable_segmentation, min_detection_confidence)

    assert bm_.static_image_mode == True
    assert bm_.model_complexity == model_complexity
    assert bm_.enable_segmentation == enable_segmentation
    assert bm_.min_detection_confidence == min_detection_confidence


# def test_apply_mask_exceptions() -> None:
#     """Test if improper mask raises error"""
#     height, width = 5, 4
#     img = [np.random.randn(height, width, 3)] * 2
#     mask = np.random.randn(height, width)
#     with pytest.raises(AssertionError) as err:
#         Segmentation.apply_masks(img, mask)
#     assert str(err.value) == "Masks should be 3 dimensional"


# def test_apply_mask_exception_depth() -> None:
#     """Test if importper depth raises error"""
#     height, width = 5, 4
#     img = [np.random.randn(height, width, 3)] * 2
#     mask = np.random.randn(height, width, 1)
#     depths = [np.random.randn(height, width)]
#     with pytest.raises(AssertionError) as err:
#         Segmentation.apply_masks(img, mask, depths)
#     assert str(err.value) == "Number of rgb and depth images should be same!"
