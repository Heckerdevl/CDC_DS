🏠 High-Precision Property Valuation Ensemble

This repository contains a production-ready machine learning pipeline for predicting residential real estate prices.
After extensive experimentation with Multimodal (Satellite Imagery + Tabular) and purely Tabular approaches, the project converges on a highly optimized tabular ensemble that delivers superior accuracy, stability, and computational efficiency.

🎯 Project Objective

The primary objective is to develop a robust and low-variance property valuation model that:

Accurately captures architectural, spatial, and neighborhood-level effects

Minimizes prediction error through careful feature engineering

Leverages heterogeneous ensemble learning rather than relying on a single model class

The final system prioritizes predictive reliability over architectural novelty, making it suitable for real-world deployment scenarios.

📊 Model Performance Summary
Model	                            R² Score	Status
Hybrid Multimodal (CNN + Tabular)	0.90      	Benchmark
Tabular Ensemble (Winning Model)	0.90+   	Production

🔍 Decision Insight

Although satellite imagery was integrated using EfficientNet-B0 during the research phase, the Tabular Ensemble consistently outperformed the multimodal approach for this dataset.

Key reasons:

High signal density already present in engineered tabular features

Visual noise introduced by satellite imagery at property-level granularity

Superior generalization and stability of tree-based ensembles on structured data

🏗️ Technical Architecture

The final pipeline consists of three tightly-coupled components: data processing, feature engineering, and a weighted ensemble regressor.

1️⃣ Data Processing & Normalization
Log Transformations

To stabilize variance and handle right-skewed distributions:

Applied log(1 + x) to:

Target variable (price)

All area-based features (sqft_living, sqft_lot, etc.)

This transformation significantly improves convergence for tree-based models.

Temporal Feature Engineering

Converted raw construction and transaction dates into:

age_at_sale — a direct proxy for physical depreciation

Renovation flags were preserved to capture post-construction value appreciation

Feature Selection Strategy

Retained high-impact predictors:

grade, latitude, longitude, waterfront, view

Removed:

Redundant identifiers

Leakage-prone or low-signal attributes

2️⃣ The Winning Ensemble Model

Final predictions are generated using a weighted blend of three complementary algorithms:

🟢 CatBoost — 40%

Handles categorical-like ordinal features (e.g., grade, view) effectively

Symmetric tree growth reduces overfitting

Strong performance on structured, medium-sized datasets

🔵 XGBoost — 40%

Captures complex non-linear interactions

Excels at minimizing residual error through level-wise boosting

Provides strong bias reduction

🟠 Random Forest — 20%

Bagging-based learner for variance reduction

Acts as a stabilizer against aggressive boosting behavior

Improves generalization under distribution shifts

Why this blend works:
Boosting models capture sharp decision boundaries, while Random Forest adds robustness—resulting in a well-balanced bias-variance tradeoff.

🧪 Multimodal Research (Exploratory Phase)

Although not used in production, a CNN-based visual pipeline was implemented and evaluated:

Backbone: EfficientNet-B0

Input: High-resolution satellite imagery

Fusion: Late fusion with tabular features

The multimodal model was retained as a benchmark, validating that visual context did not provide sufficient marginal gain over strong tabular signals for this dataset.

📂 Repository Structure
├── imagery_harvester.py        # Satellite tile downloader (research phase)
├── preprocessing.ipynb        # Deep EDA and feature engineering
├── model_training.py          # Final ensemble training & inference script
├── tabular_final_submission.csv  # Final valuation predictions

🛠️ Installation & Usage
1️⃣ Install Dependencies
pip install pandas numpy scikit-learn xgboost catboost

2️⃣ Prepare Data

Ensure the following files are present in the working directory:

train(1)(train(1)).csv

test2(test(1)).csv

3️⃣ Run Training & Inference
python model_training.py


The script will:

Train the weighted ensemble

Generate predictions

Export the final valuation file

📈 Key Insights from EDA
📍 Location Dominance

Latitude and longitude emerged as the strongest non-linear predictors, implicitly encoding neighborhood desirability, infrastructure access, and zoning effects.

🏗️ Grade Gap Effect

Properties with construction grades 11–13 show exponential price jumps, far exceeding mid-tier grades—highlighting strong quality segmentation in the market.

🔧 Renovation Premium

Renovated properties maintain a significantly higher price floor, independent of original construction year—confirming renovation as a dominant value driver.

🧠 Final Takeaway

This project demonstrates that careful feature engineering and ensemble design can outperform more complex multimodal architectures when the structured signal is strong.

Result: A stable, interpretable, and production-ready valuation model with high predictive accuracy.