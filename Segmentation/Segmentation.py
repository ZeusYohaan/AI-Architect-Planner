import os
import torch
from groundingdino.util.inference import Model
from segment_anything import sam_model_registry, SamPredictor
from typing import List
import cv2
import supervision as sv


class ImageSegmentation:
    def __init__(self):
        self.HOME = os.getcwd()
        self.SAM_ENCODER_VERSION = "vit_h"
        self.SAM_CHECKPOINT_PATH = os.path.join(self.HOME, "weights", "sam_vit_h_4b8939.pth")
        self.GROUNDING_DINO_CONFIG_PATH = os.path.join(self.HOME,
                                                       "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.GROUNDING_DINO_CHECKPOINT_PATH = os.path.join(self.HOME, "weights", "groundingdino_swint_ogc.pth")
        self.DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.grounding_dino_model = Model(model_config_path=self.GROUNDING_DINO_CONFIG_PATH,
                                          model_checkpoint_path=self.GROUNDING_DINO_CHECKPOINT_PATH)
        self.sam = sam_model_registry[self.SAM_ENCODER_VERSION](checkpoint=self.SAM_CHECKPOINT_PATH).to(
            device=self.DEVICE)

    def improvise_class_names(self, class_names: List[str]) -> List[str]:
        return [
            f"all {class_name}s"
            for class_name
            in class_names
        ]
