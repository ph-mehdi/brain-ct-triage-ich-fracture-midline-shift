# Reproduction guide

## Environment

Use a Python GPU notebook environment such as Kaggle with PyTorch, torchvision, pandas, NumPy, scikit-learn, pydicom, matplotlib, and the notebook-specific imaging libraries. Some training notebooks install `segmentation_models_pytorch` or `timm` in their setup cells. Retain the original notebook setup cells and check versions in the active Kaggle image; no fully pinned environment or frozen image was saved with this research history.

## Inputs

1. Attach the authorized CT dataset with the `Data/training`, `Data/annotations`, `Data/training_df.pkl`, and `series_targets_df.csv` layout.
2. Update each notebook's `DATASET_ROOT_CANDIDATES` if the Kaggle input mount differs from the original account or dataset name.
3. Use the same series split for comparisons. Notebook 18 reconstructs the 216/54/68 split from series targets; the other model notebooks follow the same split logic.
4. Save notebook outputs for downstream fusion. Notebook 28 expects the outputs of 18, 23, 24, and the historical `final-evaluation` run. Notebook 29 additionally expects outputs of 22 and 26.

## Suggested sequence

| Step | Notebook(s) | Output or purpose |
| --- | --- | --- |
| Explore | 01 | Inspect DICOM, metadata, annotations |
| Establish ICH baseline | 17, 18 | Compare 2D and 2.5D; save DEV slice predictions and model configuration |
| Train fracture and MLS | 23, 24 | Save series-level outputs |
| Reproduce the highest reported triage comparison | 28 | Inspect all rows in the comparison table, especially the historical-fracture row |
| Analyze alternatives | 20, 21, 22, 25, 26, 27, 29 | Component audit, calibration, architecture comparisons, gate experiment |

The historic `final-evaluation` output is not part of this repository. Thus, running the notebooks with only this checkout will **not** reproduce the 0.8188 result. Verify the upstream output identity, feature columns, series alignment, and split before citing a reproduction. For deployment, construct an inference artifact that loads available weights and reproduces the selected preprocessing and thresholds; none is represented here as complete.

The notebook copies contain no stored cell outputs. Run them against data you are authorized to use. Do not commit DICOM images, annotation tables, series-level prediction rows, model weights, secret credentials, or saved outputs from patient-derived data.
