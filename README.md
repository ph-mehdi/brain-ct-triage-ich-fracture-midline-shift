# Brain CT Triage: Intracranial Hemorrhage, Skull Fracture & Midline Shift

**Medical image analysis with DICOM preprocessing, 2D/2.5D/3D deep learning, segmentation, ordinal classification, and series-level decision calibration.**

This repository documents a research workflow for assigning a three-level triage label to a head CT series. The component predictions are intracranial hemorrhage (ICH) subtype volumes, skull fracture probability, and midline shift (MLS). A rule-based decision function combines the predictions. The work was developed in Kaggle notebooks against the IAAA Brain CT Triage Challenge data.

> **Best observed development result:** macro F1 **0.8188** and accuracy **0.8333** on **54 DEV series** (Notebook 28, using the existing fracture prediction). These are selected and calibrated on the same small DEV split. They are **not** a public leaderboard score or an independent test estimate. A final submission pipeline and external validation are not included here.

The original challenge brief in this repository describes **quadratic weighted kappa (QWK)** as the primary competition metric, with total ICH volume MAE as a tie-breaker. The DEV macro F1 above is an **internal research metric**, not QWK; no comparable official submission score is reported. See [Problem statement](docs/problem.md) and [Evaluation](docs/evaluation.md).

## What the project demonstrates

- Read and sort DICOM slices; convert pixel values to Hounsfield units using the modality transform; apply task-specific CT windows.
- Decode run-length encoded, five-subtype ICH segmentation masks and reconstruct slice context.
- Train a 2D baseline, a 2.5D EfficientNet-B4 U-Net using previous/center/next slices, and a 3D residual U-Net comparison.
- Handle partially annotated series: use all slices from confirmed ICH-negative series as background, while **never** treating unannotated slices in ICH-positive series as negative segmentation targets.
- Train a 2.5D skull-fracture classifier with bone windows, an ICH-presence classifier, and ordinal MLS classifiers for the 1, 3 and 5 mm thresholds.
- Aggregate slice predictions to series-level volumes/probabilities, apply continuity rules, and analyze the effect of each component on three-class triage macro F1.

## Data and study design

The Kaggle data layout used in the notebooks contains `Data/training/` DICOM series, `Data/annotations/` per-slice JSON annotations, `Data/training_df.pkl`, and `series_targets_df.csv`. The target table includes five ICH subtype volumes (`V_EDH`, `V_SDH`, `V_IPH`, `V_SAH`, `V_IVH`), `fracture_prob`, `MLS_mm`, and `triage_class`. The exploration notebook reports **338 series and 7,508 training metadata rows**. The shared split used by the modeling notebooks is **216 TRAIN / 54 DEV / 68 held-out series**; the fusion experiments below report DEV results only. See [Data and preprocessing](docs/data.md).

The dataset, images, patient/series identifiers, model checkpoints, raw predictions, and Kaggle output archives are **not stored in this repository**. Access and reuse of the original competition data must follow its own terms.

## Results on the common DEV split

| Experiment | Metric | Observed result | Scope |
| --- | --- | ---: | --- |
| 2D ICH with expanded negatives (17) | Best mean segmentation Dice | 0.4603 | Model selection on DEV |
| 2.5D ICH, EfficientNet-B4 U-Net (18) | Best mean segmentation Dice | 0.4990 | Model selection on DEV |
| 3D residual U-Net (25) | Best center-slice Dice | 0.3111 | Different 3D evaluation path; not a direct architectural ranking |
| Fracture 2.5D series classifier (23) | Best series F1 | 0.7500 | Threshold/model selection on DEV |
| ICH presence gate (26) | Best series F1 / recall | 0.9057 / 0.9600 | Component result, not final triage |
| MLS ordinal EfficientNet-B2 (24) | Best mean threshold F1 / bin accuracy | 0.9260 / 0.8333 | DEV; threshold F1 and bin accuracy are different measures |
| MLS ordinal EfficientNet-B4 (27) | Best mean threshold F1 / bin accuracy | 0.9256 / 0.8519 | Better bin accuracy, marginally lower best mean threshold F1 than B2 |
| Initial calibrated triage (21) | Three-class macro F1 | 0.8026 | 54 DEV series |
| **ICH B4 + ordinal MLS B2 + existing fracture (28)** | **Three-class macro F1 / accuracy** | **0.8188 / 0.8333** | **Best recorded DEV configuration** |
| ICH B4 + ordinal MLS B2 + new fracture (28) | Three-class macro F1 | 0.7986 | The new fracture component reduced triage F1 in this comparison |
| Gated B4/B5 fusion experiment (29) | Three-class macro F1 | 0.7487 | Staged search produced a worse DEV configuration |

These numbers were transcribed from the executed notebook outputs before those outputs were removed from the public-ready notebook copies. The **B4 MLS model was not yet evaluated in the best Notebook 28 triage pipeline**. Results are exploratory: repeated DEV tuning, class imbalance, and the small split can make the selected F1 optimistic. The diagnostic audit (20) also reads a separate saved `TEST_LOCKED` prediction file, so the repository does not present that split as a blind external validation. See [Evaluation and limitations](docs/evaluation.md).

## Repository map

| Path | Purpose |
| --- | --- |
| [`notebooks/`](notebooks/) | Data exploration, model training, component audits, and DEV fusion experiments |
| [`docs/data.md`](docs/data.md) | Data fields, annotations, CT transforms, missing-label handling, and split |
| [`docs/problem.md`](docs/problem.md) | Original challenge objective and distinction between official and internal metrics |
| [`docs/methods.md`](docs/methods.md) | Architectures, training targets, aggregation, and decision rule |
| [`docs/evaluation.md`](docs/evaluation.md) | Metric definitions, experiment provenance, and limits |
| [`docs/reproduce.md`](docs/reproduce.md) | Kaggle input configuration and execution sequence |
| [`src/brain_ct_triage/triage.py`](src/brain_ct_triage/triage.py) | Standalone implementation of the decision rule used in fusion experiments |
| [`tests/`](tests/) | Boundary tests for the rule |
| [`docs/github.md`](docs/github.md) | Suggested repository description and searchable GitHub topics |

The included notebooks are the **source code**, with saved cell outputs and execution state removed to avoid exposing case identifiers or raw dataset details. They retain their Kaggle-specific input paths and need the corresponding competition data and saved upstream outputs. Notebook 30 was supplied as an incomplete calibration scaffold with unset input paths and no final metric; it is intentionally omitted until a completed run is available.

## Reproduction

Use a GPU-enabled Kaggle environment, attach the competition dataset and the saved outputs called for by each notebook, then follow [the execution guide](docs/reproduce.md). The smallest path to the reported triage result is: train/run 18, 23, and 24; attach their saved outputs and the historical `final-evaluation` output; run 28. Notebook 28 evaluates both the existing and the newly trained fracture component. The historical fracture predictions required for the best 0.8188 result are an external upstream dependency; they are not reconstructed by the provided notebooks alone.

## Scope

This is an experimental portfolio project, **not a clinical device**. No prospective evaluation, calibration on an independent cohort, robustness study across institutions, or deployment validation is documented here. Source code can be reviewed without obtaining or redistributing the CT data.

For the standalone rule, run `python -m pip install -e .` and `python -m unittest discover -s tests` from the repository root. The model-training notebooks have additional Kaggle dependencies described in the reproduction guide.
