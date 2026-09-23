# Brain CT Triage: Hemorrhage, Skull Fracture and Midline Shift

**Medical image analysis of non-contrast head CT using DICOM preprocessing, 2D/2.5D/3D deep learning, segmentation, ordinal classification and series-level model fusion.**

This project processes variable-length CT series to estimate five intracranial hemorrhage (ICH) subtype volumes, skull fracture probability and midline shift (MLS). A deterministic decision rule combines these estimates into three study-level triage categories. The repository contains model development, error analysis and calibration experiments in PyTorch notebooks, plus a standalone implementation of the decision rule.

## Technical work

- **Imaging pipeline:** sorted DICOM slices by spatial position; converted pixels to Hounsfield units; applied blood, bone and brain CT windows; decoded run-length encoded subtype masks and prepared neighboring-slice inputs.
- **ICH segmentation:** trained a 2D baseline and 2.5D EfficientNet-B4 U-Net using previous/current/next slices; compared a B5 encoder and a 3D residual U-Net. Derived series-level subtype volumes from slice masks and pixel spacing.
- **Partial annotations:** expanded background examples from confirmed negative series without labeling unannotated slices in positive series as negative.
- **Fracture and MLS:** trained a bone-window 2.5D fracture classifier, an ICH-presence model, and EfficientNet-B2/B4 ordinal models for MLS thresholds of 1, 3 and 5 mm.
- **Evaluation:** aggregated slice outputs across each series, evaluated continuity filtering and top-k probabilities, and compared component changes on a common DEV split.

## Data and results

The IAAA brain CT data used in these experiments comprises DICOM series, per-slice JSON annotations and series-level targets for EDH, SDH, IPH, SAH and IVH volumes, fracture probability, MLS and triage category. The exploration notebook reported **338 series** and **7,508 metadata rows**; the modeling split was **216 TRAIN / 54 DEV / 68 held-out series**. See [Data and preprocessing](docs/data.md).

| DEV experiment | Observed metric |
| --- | ---: |
| 2.5D EfficientNet-B4 ICH segmentation | Best mean Dice **0.4990** |
| 2.5D fracture classification | Best series F1 **0.7500** |
| Ordinal MLS EfficientNet-B2 / B4 | Mean threshold F1 **0.9260 / 0.9256** |
| ICH + ordinal MLS B2 + existing fracture estimate | Three-class macro F1 **0.8188**, accuracy **0.8333** |

The triage result was **selected and calibrated on the same 54 DEV series**. It is a local development statistic, not an independently validated estimate. The B4 MLS model achieved higher bin accuracy than B2, but was not integrated into the best recorded triage configuration. The historical fracture estimates needed for the 0.8188 row are an upstream dependency not reconstructed by this repository alone. Full experiment provenance and limitations are in [Evaluation](docs/evaluation.md).

## Repository guide

| Path | Contents |
| --- | --- |
| [`notebooks/`](notebooks/) | Exploration, training, component comparisons and fusion experiments |
| [`docs/data.md`](docs/data.md) | Input schema, CT transforms, annotation policy and split |
| [`docs/methods.md`](docs/methods.md) | Model architectures, outputs and aggregation |
| [`docs/evaluation.md`](docs/evaluation.md) | Metric definitions, recorded experiments and caveats |
| [`docs/reproduce.md`](docs/reproduce.md) | Runtime dependencies and execution order |
| [`docs/problem.md`](docs/problem.md) | Imaging task and prediction targets |
| [`src/brain_ct_triage/triage.py`](src/brain_ct_triage/triage.py) | Deterministic series-level decision function |
| [`tests/`](tests/) | Decision-boundary tests |

The notebooks are source copies with saved outputs removed. Their original input paths refer to mounted data and saved upstream outputs. The data, case identifiers, model weights and raw predictions are not distributed here. Use the dataset only under its applicable terms. Notebook 30 has no completed calibration result and is not presented as an experiment.

## Running the project

The standalone rule can be checked with `python -m pip install -e .` followed by `python -m unittest discover -s tests`. Model notebooks need a GPU environment, the authorized CT dataset and specific upstream outputs; see [Reproduction](docs/reproduce.md). The 0.8188 configuration is not reproducible from this checkout alone because its historical fracture estimates are absent.

This is exploratory research code and has not undergone prospective, external-site or clinical deployment validation.
