# Problem Statement

The **IAAA Competition 2026: Brain CT Triage Challenge** focuses on developing an automated system for triaging non-contrast brain CT examinations based on clinically meaningful imaging findings.

In emergency neuroradiology, brain CT studies must often be reviewed quickly to identify patients with potentially serious abnormalities such as intracranial hemorrhage, skull fracture, or significant mass effect. The main objective of this challenge is therefore to analyze a complete CT study and estimate the imaging findings that determine how urgently the case should be prioritized.

## Input

The input to the model is a **complete non-contrast brain CT series in DICOM format**.

Each study consists of multiple axial CT slices, and the number of slices is not necessarily fixed across studies. Therefore, the model must be able to process **variable-length CT series** and integrate information across the entire examination rather than making a decision from a single image.

## Prediction Task

The task is not formulated as a direct three-class classification problem.

Instead, the model must predict a set of clinically interpretable intermediate variables for each CT study:

- `V_EDH` — total epidural hemorrhage volume in mL
- `V_SDH` — total subdural hemorrhage volume in mL
- `V_IPH` — total intraparenchymal/intracerebral hemorrhage volume in mL
- `V_SAH` — total subarachnoid hemorrhage volume in mL
- `V_IVH` — total intraventricular hemorrhage volume in mL
- `fracture_prob` — probability that at least one skull fracture is present
- `MLS_mm` — midline shift at the level of the foramen of Monro, measured in millimeters

The hemorrhage targets represent the **total volume of each hemorrhage subtype across the entire CT study**, including all lesions belonging to that subtype.

These predictions require the model to combine several related abilities: identifying hemorrhage, distinguishing hemorrhage subtypes, estimating lesion burden across slices, detecting skull fractures, and assessing intracranial mass effect.

## Final Output

The predicted intermediate variables are converted into one of three study-level triage categories:

- **0 — Non-urgent**
- **1 — Urgent**
- **2 — Critical**

The final triage label is not predicted directly by the neural network. Instead, a **fixed deterministic triage function** provided by the competition organizers maps the predicted imaging quantities to the final triage class.

As a result, the overall problem can be summarized as:

```text
Non-contrast Brain CT Series
            ↓
     Model Prediction
            ↓
Hemorrhage Volumes
Skull Fracture Probability
Midline Shift
            ↓
 Fixed Triage Function
            ↓
Non-urgent / Urgent / Critical
```

## Objective

The objective is to build a model that can extract reliable, study-level clinical information from a complete brain CT examination and use those predictions to produce accurate emergency triage.

A successful solution must therefore do more than simply detect whether an abnormality is present. It must also estimate the **type, extent, and severity** of the relevant findings, while remaining robust to variations in CT series length and imaging appearance.

This formulation makes the problem a **multi-task, study-level medical imaging problem** rather than a conventional image classification task.

## Evaluation

The primary evaluation metric is **Quadratic Weighted Kappa (QWK)** between the predicted triage class and the ground-truth triage class.

QWK is particularly suitable for this task because the triage labels are ordinal:

```text
Non-urgent < Urgent < Critical
```

and larger classification errors are penalized more strongly than smaller ones.

For example, predicting a critical case as non-urgent is considered a more severe error than confusing an urgent case with a critical one.

If two submissions obtain the same QWK score, the **Mean Absolute Error (MAE) of total intracranial hemorrhage volume** is used as the tie-breaking metric.

Therefore, the challenge ultimately evaluates both:

1. **how accurately the predicted imaging findings reproduce the correct clinical triage**, and
2. **how accurately the model quantifies the overall intracranial hemorrhage burden**.

The central problem addressed in this repository is therefore:

> **How can a deep learning model process a variable-length non-contrast brain CT study and accurately estimate intracranial hemorrhage volumes, skull fracture probability, and midline shift in order to support reliable automated triage into non-urgent, urgent, and critical cases?**
