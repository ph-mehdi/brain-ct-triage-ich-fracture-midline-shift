# Challenge objective

The IAAA Brain CT Triage Challenge asks a model to analyze a complete, variable-length non-contrast DICOM brain CT series. It predicts clinically interpretable intermediate findings: total volume in milliliters for each of five intracranial hemorrhage subtypes (EDH, SDH, IPH, SAH, IVH), skull fracture probability, and midline shift in millimeters at the foramen of Monro. A fixed competition decision function maps these quantities to non-urgent (0), urgent (1), or critical (2) triage.

The original problem statement in this repository lists **quadratic weighted kappa (QWK)** on the ordinal triage labels as the primary official evaluation metric and **mean absolute error of total ICH volume** as the tie-breaker. The development experiments in this repository report **macro F1**, a different metric selected for local analysis. They do not establish an official QWK score. Consult the competition's current rules when preparing any submission.

This project investigates DICOM preprocessing, hemorrhage segmentation and volume estimation, fracture classification, ordinal midline-shift thresholds, and series-level aggregation. The available notebooks document experimental model development; they are not a validated clinical system.
