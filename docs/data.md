# Dataset and preprocessing

## Input organization

The modeling notebooks use the IAAA brain CT dataset, provided in a hosted notebook environment. They locate a `Data` directory with:

```text
Data/
  training/<series_id>/*.dcm
  annotations/<series_id>/<SOPInstanceUID>.json
  training_df.pkl
series_targets_df.csv
```

The actual dataset mount differs among notebooks; inspect each notebook's `DATASET_ROOT_CANDIDATES` and update it to the attached Kaggle dataset. No dataset bytes are bundled here. The exploration notebook reported 338 series and 7,508 metadata rows. The series-level target table contains five ICH volumes, fracture probability, MLS in millimeters, and triage class. `training_df.pkl` provides per-slice metadata and image spacing. The annotation JSON supplies ICH run-length encoded masks, fracture boxes, and/or MLS keypoints where present. Missing annotation JSON does **not** universally mean a negative slice.

## CT handling

1. Read DICOM pixels and apply the modality LUT or rescale slope/intercept to obtain Hounsfield units.
2. Order slices by projected `ImagePositionPatient` along the orientation normal when available; otherwise use `InstanceNumber`.
3. Clip and scale intensities with a task-specific window. The main ICH model uses a blood window centered at 45 HU with width 100 HU; the fracture classifier uses a bone window centered at 600 HU with width 2,800 HU. The ordinal MLS model uses brain-window context as defined in its notebook.
4. Build three-channel 2.5D samples from the previous, current, and next slices. Resize and normalize using the training notebook's configuration. The ICH U-Net predicts the center slice.
5. Decode ICH masks from JSON RLE and map the five labels to EDH, SDH, IPH, SAH, and IVH. Volumetric estimates use mask area, pixel spacing, and slice thickness/spacing as implemented by the notebook.

## Annotation policy

For ICH segmentation, all slices from series with **zero ground-truth ICH volume** may serve as background targets even if the slice has no JSON. In series with any ICH, only annotated slices can serve as segmentation targets. An unannotated positive-series slice may provide neighboring image context, but cannot be assigned a synthetic negative mask. The fracture classifier uses an analogous expanded-negative policy based on series-level fracture status. MLS training uses slices with usable keypoint annotations for the threshold targets.

This negative expansion uses the **series labels during training**. It is an annotation strategy, not an inference-time access to ground truth. Leakage can occur if a series or patient is shared between splits; the split reconstruction and any additional patient-level deduplication should be independently audited before treating the score as generalization evidence.

## Split

The common target split in Notebook 18 is 216 TRAIN, 54 DEV, and 68 held-out series. The README results were selected or calibrated on the 54-series DEV subset. Inspect the exact split-generation code in Notebook 18 before reproducing model comparisons; independent tests of cross-site or patient-level generalization have not been provided.
