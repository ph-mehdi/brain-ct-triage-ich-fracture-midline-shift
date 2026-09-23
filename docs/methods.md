# Methods

## Intracranial hemorrhage

Notebooks 17 and 18 compare single-slice 2D and neighboring-slice 2.5D segmentation with expanded negatives. The main 2.5D experiment uses a six-class U-Net with EfficientNet-B4 encoder: background and five hemorrhage subtypes. Three blood-window images become the input channels. A class-specific pixel-confidence threshold and continuity filtering turn slice masks into series volumes. The selected `all2` profile requires a contiguous run of two positive slices for each subtype in the Notebook 28 fusion search.

Notebook 22 examines an EfficientNet-B5 variant; Notebook 25 trains a 3D residual U-Net. Their presence documents the architectural comparison, not a claim that the larger networks improved the final triage score. Notebook 26 trains a separate 2.5D ICH-presence classifier; Notebook 29 studies its effect as a gate with a volume override. The highest recorded DEV triage configuration does not use this gate.

## Skull fracture

Notebook 23 builds a 2.5D classifier using previous/center/next bone-window slices and positive-slice annotations, with expanded negatives from confirmed fracture-negative series. It aggregates slice scores to a series probability and tunes an aggregation/threshold on DEV. Its stand-alone series F1 increased, but substituting it into the best Notebook 28 triage configuration reduced macro F1. Consequently the best recorded triage result retains the **historical fracture prediction** in the upstream evaluation output.

## Midline shift

Notebooks 24 and 27 predict slice relevance and ordinal probabilities for `MLS >= 1`, `>= 3`, and `>= 5` mm. Their backbones are EfficientNet-B2 and B4 respectively. Slice probabilities are combined with max or top-k aggregation to determine a series-level MLS bin. This targets the triage rule's decision boundaries. Notebook 28 calibrates the B2 output on DEV; B4 has a component bin-accuracy result but no reported integration into the best triage configuration.

## Series-level triage

The fusion notebooks convert the five predicted hemorrhage volumes, fracture probability, and MLS value to classes 0, 1, or 2 using the decision rule in [`src/brain_ct_triage/triage.py`](../src/brain_ct_triage/triage.py). Thresholds include EDH 30 mL, SDH or IPH 70 mL, total ICH 60 mL, and selected interactions with fracture and MLS at 3 or 5 mm. This is the **implemented decision rule in the supplied fusion notebooks**, not an independently validated clinical triage policy.

The search is staged on a shared 54-series DEV set. Notebook 28 yielded its best result using ICH `all2`, the B2 MLS `top3` score for 3 mm at a 0.67 threshold, the `top5` score for 5 mm at a 0.89 threshold, and the pre-existing fracture prediction. Those cutoffs were selected on DEV and should not be interpreted as probability calibration for unseen sites.
