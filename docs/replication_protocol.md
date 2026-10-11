# Replication Protocol Notes

**Target:** Zabërgja et al., *Tabular Data: Is Deep Learning All You Need?*, arXiv:2402.03970v3, 5 October 2025.  
**Status:** Initial extraction from Section 3.2 (printed page 4–5) and Appendix A.1 (printed page 14). This is not yet a complete implementation specification.

## 1. Benchmark and dataset coverage

The preprint states that the study uses OpenML-CC18, described as a 72-dataset classification benchmark. It says four datasets were excluded due to memory issues, leaving 68 datasets in the analysis. The paper points to Appendix E for the full dataset list.

The paper describes the benchmark data as covering binary and multiclass classification, with approximately 500–100,000 instances and 5–3,073 features.

**Implementation requirement:** verify our dataset manifest against Appendix E. Do not assume that a dataset list copied from the later TMLR repository is identical to the original preprint's final list.

## 2. Preprocessing (Section 3.2, printed page 4)

The paper states:
- By default, numerical features receive a scikit-learn quantile transformation.
- Categorical features receive ordinal encoding, following prior work.
- A single preprocessing approach is used across methods where possible.
- TP-BERTa and CARTE are named as examples that require a different approach.
- For methods whose library implementation makes preprocessing difficult to modify, the authors use the preprocessing strategy from the original method.
- Batch size is not tuned because of memory constraints. It is selected heuristically based on the number of features; batch sizes may differ between datasets but are kept consistent across methods.

### Details not specified in this paragraph

The paragraph does not fully specify:
- the exact scikit-learn quantile-transformer parameters (for example, output distribution and quantile count);
- the exact ordinal-encoder settings, including unseen-category handling;
- whether each transform is fit separately inside every inner training fold and then applied to its validation fold;
- the precise heuristic mapping feature count to batch size;
- the full per-method list of preprocessing exceptions.

These must be checked against Appendix A, method-specific papers/code, and/or author clarification. We must not silently invent these settings and describe them as paper-specified.

## 3. Nested cross-validation and hyperparameter optimization (Section 3.2, printed pages 4–5; Appendix A.1, printed page 14)

The paper specifies:
- Outer folds: **K = 10**.
- Inner folds for HPO: **J = 9**.
- Maximum HPO trials: **T = 100**, or stop when the maximum duration of **23 hours** is reached.
- HPO implementation: Optuna with the Tree-structured Parzen Estimator (TPE) sampler.
- For each outer fold, split the data into an outer training partition and a held-out outer test partition.
- For every HPO trial, evaluate the sampled hyperparameter configuration on the nine inner folds of the outer training partition.
- Use the mean performance across the nine inner validation folds as the Optuna objective.
- Select the best configuration after the trial budget or time budget is exhausted.
- Fit the final model on the full outer training partition (i.e., all data available outside that outer test fold), then evaluate once on the held-out outer test fold.
- Aggregate the outer-test performance by taking the mean over the ten outer folds.
- Use the official hyperparameter search spaces from the respective method papers.
- The paper treats the number of training iterations as a hyperparameter, describing this as an implicit alternative to early stopping.

The prose in Section 3.2 says the selected model is trained on the combined training and validation splits. Appendix A.1 expresses this as refitting on the outer training partition after HPO. These descriptions are consistent if “training + validation” means the full outer-training data that had been partitioned into inner training/validation folds during tuning. The outer test fold must remain untouched until final evaluation.

## 4. Primary metric

The paper reports **mean ROC-AUC across the 10 outer test folds**, motivated by the class imbalance present in OpenML-CC18.

For multiclass datasets, the exact ROC-AUC averaging convention must be confirmed from the implementation or additional paper details. Do not assume binary ROC-AUC code is sufficient.

## 5. Compute and scale

The preprint reports experiments on NVIDIA RTX 2080 Ti GPUs with 11 GB memory. It estimates up to 68,000 different models evaluated per algorithm, approximately 900,000 individual evaluations, and about 8 million evaluations across 17 methods.

Our local hardware and available compute are substantially smaller. A reduced-trial smoke test is useful for engineering validation but is **not** an exact replication of the published compute budget. Any later resource-constrained experiments must label their deviations explicitly.

## 6. Current pilot dataset (engineering validation only)

Balance-Scale (OpenML dataset ID 11) was downloaded into separate feature and target CSV files and inspected:
- Features: 625 rows × 4 columns.
- Target: 625 rows; classes R = 288, L = 288, B = 49.
- Missing values: none observed in the feature or target CSVs.
- Feature columns: left-weight, left-distance, right-weight, right-distance.

This dataset is currently a **pipeline smoke-test candidate**. Its inclusion in the exact 68-dataset list must be checked against Appendix E before using it as a benchmark replication result.

## 7. Open questions before implementation

- [ ] Extract the complete dataset list and exclusions from Appendix E.
- [ ] Check Appendix A and method-specific references for the exact preprocessing parameters.
- [ ] Confirm fold-generation method, stratification, random seeds, and any OpenML task split requirements.
- [ ] Confirm the multiclass ROC-AUC convention.
- [ ] Confirm per-method preprocessing and batch-size exceptions.
- [ ] Ask the authors whether the original source code/configuration is archived and how the original preprint relates to the later TMLR paper.
- [ ] Separate paper-specified settings from our explicit implementation choices in configuration and reports.

## References

- Original preprint: https://arxiv.org/abs/2402.03970
- Later TMLR paper for comparison only: https://openreview.net/forum?id=I8BIGp4XOb
- Later paper's repository (not assumed to be the original implementation): https://github.com/machinelearningnuremberg/Tabular-Study
