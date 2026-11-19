"""
Program 7 : Hyper-parameter tuning for a Machine Learning model (CO4)
Aim   : Find the best hyper-parameters (settings chosen BEFORE training, e.g.
        C and gamma of an SVM, number of trees of a Random Forest).
Data  : Wine data set (178 samples, 13 features, 3 classes) - built into scikit-learn.
Methods : 1. GridSearchCV        - tries EVERY combination with 5-fold cross-validation
          2. RandomizedSearchCV  - tries a random sample of combinations (faster)
Steps : split data -> baseline model -> tune -> compare on unseen test data
Install : pip install scikit-learn numpy pandas
"""
import numpy as np
import pandas as pd
from scipy.stats import randint
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

if __name__ == "__main__":
    data = load_wine()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, stratify=data.target, random_state=42)
    print("HYPER-PARAMETER TUNING")
    print(f"Training samples: {len(X_train)}   Test samples: {len(X_test)}   Features: {X_train.shape[1]}\n")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # ---------- Model 1 : SVM with Grid Search ----------
    svm_base = Pipeline([("scale", StandardScaler()), ("svm", SVC())])
    svm_base.fit(X_train, y_train)
    base_acc = accuracy_score(y_test, svm_base.predict(X_test))
    # a deliberately poor setting to show why tuning matters
    svm_bad = Pipeline([("scale", StandardScaler()), ("svm", SVC(kernel="sigmoid", C=0.01))]).fit(X_train, y_train)
    print("1) SVM + GridSearchCV")
    print(f"   Poor setting (sigmoid kernel, C=0.01) test accuracy : {accuracy_score(y_test, svm_bad.predict(X_test)):.3f}")
    print(f"   Default SVM test accuracy                          : {base_acc:.3f}")

    param_grid = {"svm__C": [0.1, 1, 10, 100],
                  "svm__gamma": ["scale", 0.1, 0.01, 0.001],
                  "svm__kernel": ["rbf", "linear", "poly"]}
    grid = GridSearchCV(svm_base, param_grid, cv=cv, scoring="accuracy", n_jobs=-1)
    grid.fit(X_train, y_train)
    n_combo = len(grid.cv_results_["params"])
    print(f"   Combinations tried : {n_combo}  x 5 folds = {n_combo * 5} model fits")
    print("   Best parameters    :", grid.best_params_)
    print(f"   Best cross-validation accuracy : {grid.best_score_:.3f}")
    print(f"   Test accuracy of tuned SVM     : {accuracy_score(y_test, grid.predict(X_test)):.3f}")

    res = pd.DataFrame(grid.cv_results_).sort_values("rank_test_score").head(5)
    print("\n   Top 5 combinations:")
    print(res[["params", "mean_test_score", "std_test_score"]].to_string(index=False))

    # ---------- Model 2 : Random Forest with Randomized Search ----------
    print("\n2) Random Forest + RandomizedSearchCV")
    rf_base = RandomForestClassifier(random_state=42).fit(X_train, y_train)
    print(f"   Default Random Forest test accuracy : {accuracy_score(y_test, rf_base.predict(X_test)):.3f}")
    dist = {"n_estimators": randint(50, 400), "max_depth": [None, 3, 5, 8, 12],
            "min_samples_split": randint(2, 10), "min_samples_leaf": randint(1, 5),
            "max_features": ["sqrt", "log2", None]}
    rnd = RandomizedSearchCV(RandomForestClassifier(random_state=42), dist, n_iter=25, cv=cv,
                             scoring="accuracy", random_state=42, n_jobs=-1)
    rnd.fit(X_train, y_train)
    print("   Combinations tried : 25 (random sample) x 5 folds")
    print("   Best parameters    :", rnd.best_params_)
    print(f"   Best cross-validation accuracy : {rnd.best_score_:.3f}")
    print(f"   Test accuracy of tuned Random Forest : {accuracy_score(y_test, rnd.predict(X_test)):.3f}")

    print("\nClassification report of the tuned SVM on the test set:")
    print(classification_report(y_test, grid.predict(X_test), target_names=data.target_names))
