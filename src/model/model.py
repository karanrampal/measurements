"""Model for body measurement prediction"""

from typing import List, Tuple

import mediapipe as mp
import numpy as np
from mediapipe.python.solutions.pose import PoseLandmark

mp_pose = mp.solutions.pose


class BodyMeasurement:
    """Body measurement class to extrac varous measurements
    Args:
        model_complexity: Model complexity (can be 0, 1, 2)
        enable_segmentation: Enable segmentation
        min_detection_confidence: Minimum detection score
    """

    def __init__(
        self,
        model_complexity: int = 2,
        enable_segmentation: bool = False,
        min_detection_confidence: float = 0.5,
    ) -> None:
        self.static_image_mode = True
        self.model_complexity = model_complexity
        self.enable_segmentation = enable_segmentation
        self.min_detection_confidence = min_detection_confidence

    def get_world_landmarks(self, image: np.ndarray) -> PoseLandmark:
        """Convert images to landmarks in world co-ordinates"""
        with mp_pose.Pose(
            static_image_mode=self.static_image_mode,
            model_complexity=self.model_complexity,
            enable_segmentation=self.enable_segmentation,
            min_detection_confidence=self.min_detection_confidence,
        ) as pose:
            results = pose.process(image)
        return results.pose_world_landmarks.landmark

    def distance(self, landmark1: PoseLandmark, landmark2: PoseLandmark) -> float:
        """Find euclidean distance between two landmarks"""
        return (
            (landmark1.x - landmark2.x) ** 2
            + (landmark1.y - landmark2.y) ** 2
            + (landmark1.z - landmark2.z) ** 2
        ) ** 0.5

    def leg_measurement(self, landmarks: PoseLandmark) -> Tuple[float, float]:
        """Extrat leg measurement"""
        left_leg = self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_HIP],
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
        ) + self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE],
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
        )
        right_leg = self.distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE],
        ) + self.distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE],
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE],
        )
        return left_leg, right_leg

    def torso_measurement(self, landmarks: PoseLandmark) -> Tuple[float, float]:
        """Extrat torso measurement"""
        left_torso = self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
            landmarks[mp_pose.PoseLandmark.LEFT_HIP],
        )
        right_torso = self.distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
        )
        return left_torso, right_torso

    def chest_measurement(self, landmarks: PoseLandmark) -> float:
        """Extrat chest measurement"""
        chest = self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        )
        return chest

    def arm_measurement(self, landmarks: PoseLandmark) -> Tuple[float, float]:
        """Extrat arm measurement"""
        left_arm = self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
        ) + self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
        )
        right_arm = self.distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
        ) + self.distance(
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
        )
        return left_arm, right_arm

    def hip_measurement(self, landmarks: PoseLandmark) -> float:
        """Extrat hip measurement"""
        hip = self.distance(
            landmarks[mp_pose.PoseLandmark.LEFT_HIP],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
        )
        return hip

    def get_features(self, landmarks: PoseLandmark) -> List[float]:
        """Manual feature extraction"""
        left_leg, right_leg = self.leg_measurement(landmarks)
        leg = max(left_leg, right_leg)

        left_torso, right_torso = self.torso_measurement(landmarks)
        torso = max(left_torso, right_torso)

        chest = self.chest_measurement(landmarks)

        left_arm, right_arm = self.arm_measurement(landmarks)
        arm = max(left_arm, right_arm)

        hip = self.hip_measurement(landmarks)

        return [leg, torso, chest, arm, hip]
