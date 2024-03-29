
## AI-Builderplus Floor Plan

### Concepts Used
- Grounding DINO
- SAM by Meta
- Computer Vision
- AWS 

### Brief Overview
- The input image is a floor plan(ranging from basic to advanced), it undergoes the following pre-processing processes:-
- Masking: The code masks all possible objects in the image using SAM
- Object-Classification: Using our pre-trained GroundingDINO model, unnecessary object-mask are selected and removed
- Fine-Noise-Removal: This computer vision code using OpenCV removes finer noise in the image
- Finally the processed image only contains the walls and doors
- This final processed image is then passed to a blender which converts it to a 3D model
