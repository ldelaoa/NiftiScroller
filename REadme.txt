REadme 
SliceViewer is an interactive Python tool for visualizing 3D medical image volumes (e.g., CT scans) along with ground truth and deep learning segmentation overlays. It supports axial, coronal, and sagittal views with intuitive keyboard and mouse controls.

🚀 Features
View 3D medical volumes slice-by-slice in:
Axial
Coronal
Sagittal
Overlay:
Ground Truth (GT) contours
Deep Learning (DL) segmentation masks
Interactive controls for toggling overlays and navigating slices

🎮 Controls
Action	Key / Mouse
Next slice	Scroll up / ↑
Previous slice	Scroll down / ↓
Toggle GT contours	G or mouse click
Toggle DL overlay	D
Switch view (plane)	V

📦 Requirements
numpy
matplotlib
scikit-image

📐 Data Format
All input arrays must have the same shape: (depth, height, width).

ct_data: 3D NumPy array of grayscale image data
seg_data: 3D binary mask for ground truth segmentation
dl_data: 3D mask (can be probabilistic or labeled) from a deep learning model

📌 Notes
The viewer starts in axial view by default.
All events (scroll, click, keypress) affect the current view.
Contours are extracted using skimage.measure.find_contours.