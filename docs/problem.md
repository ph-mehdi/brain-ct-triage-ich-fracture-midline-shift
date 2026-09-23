# Task and prediction targets

This project analyzes complete, variable-length non-contrast DICOM brain CT series. For each series, the pipeline estimates five hemorrhage subtype volumes in milliliters (EDH, SDH, IPH, SAH and IVH), skull fracture probability and midline shift in millimeters at the foramen of Monro. A fixed decision function maps those intermediate predictions to non-urgent (0), urgent (1) or critical (2) categories.

The data include DICOM images, per-slice JSON annotations and series-level targets. Evaluation in this repository focuses on segmentation Dice, binary series F1, ordinal MLS thresholds and three-class macro F1. The best observed triage figure is a development-set selection statistic, not external validation or evidence of clinical readiness.
