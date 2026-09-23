# Evaluation and provenance

## Official competition metric versus research metric

The original challenge brief in this GitHub repository identifies quadratic weighted kappa (QWK) for ordinal triage as the official metric and total ICH volume MAE as a tie-breaker. The experiments below instead selected configurations by three-class macro F1 on the shared DEV split. Macro F1, accuracy, component F1 and Dice do not represent a QWK leaderboard result. No official submission score is established by these experiments.

## Metrics

- **Triage macro F1**: arithmetic mean of F1 for the three triage classes, as computed in the fusion notebooks with `labels=[0, 1, 2]` and `zero_division=0`.
- **Segmentation Dice**: overlap of predicted and annotated ICH masks on the notebook's DEV evaluation slices. The 3D center-slice measurement has its own sampling/evaluation path.
- **Series F1**: binary F1 after aggregating slice probabilities for ICH presence or fracture.
- **Ordinal MLS metrics**: mean F1 over the three individual thresholds and accuracy of the derived series-level shift bins.

Metrics from these different tasks should not be compared as if they are one score.

## Evidence map

| Claim in README | Original executed source |
| --- | --- |
| 338 series / 7,508 metadata rows | 01, dataset inspection output |
| 216 / 54 / 68 split | 18, split reconstruction output |
| 2D Dice 0.4603 | 17, best epoch 23 |
| 2.5D Dice 0.4990 | 18, best epoch 25 |
| 3D center Dice 0.3111 | 25, best epoch 27 |
| Fracture series F1 0.7500 | 23, best training epoch and tuned series prediction |
| ICH-presence F1 0.9057 and recall 0.9600 | 26, aggregation search output |
| MLS B2 F1 0.9260 and bin accuracy 0.8333 | 24, training summary and bin evaluation |
| MLS B4 F1 0.9256 and bin accuracy 0.8519 | 27, training summary and bin evaluation |
| Calibrated triage macro F1 0.8026 | 21, final comparison |
| Best recorded triage macro F1 0.8188 | 28, `ICH all2 + optimized Notebook24 ordinal MLS + current fracture` |
| New fracture substitution 0.7986 | 28, `Final: ICH + ordinal MLS + new fracture` |
| Gated experiment 0.7487 | 29, final comparison |

These are **DEV-selected experiments**, including model checkpoints, thresholds, and postprocessing. Notebook 28's final cell prints 0.7986 for the newly substituted fracture model; the **higher 0.8188 result is the preceding row in its comparison table**, which keeps the historical fracture model. The B4 MLS model's bin accuracy rises from 0.8333 to 0.8519; its best mean threshold F1 changes from 0.9260 to 0.9256. Neither component result demonstrates a better final triage score by itself.

## Limitations

The same 54 DEV series were used repeatedly for architecture and threshold selection. The best observed result is therefore a development selection statistic, not a confidence-bounded estimate of prospective performance. Several positive classes, especially fracture, are rare. A single case can materially alter F1. Training and fusion depend on upstream data and output files that cannot be reconstructed from this source-only repo without the competition dataset and historical baseline outputs. No hidden leaderboard number, final submission artifact, independent external site, or clinical validation is reported.

The exploratory dependency notebook (20) reads saved `TEST_LOCKED` predictions and reports diagnostics for that split. For that reason, the repository makes no claim that its full research history preserved a wholly unseen test cohort. Notebook 30, supplied later as a scaffold, contained unset paths and no computed final score; it has not been included as a completed result.
