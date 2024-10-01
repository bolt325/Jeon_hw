import numpy as np
from sklearn import datasets, model_selection
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    wdbc = datasets.load_breast_cancer()

    param_grid = {
        'learning_rate': [0.01, 0.05],
        'n_estimators': [500, 1000],
        'max_depth': [3, 4],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'subsample': [0.8, 0.9],
        'max_features': ['sqrt'],
        'max_leaf_nodes': [None, 10]
    }

    grid_search = GridSearchCV(
        estimator=GradientBoostingClassifier(
            random_state=42,
            n_iter_no_change=10,
            validation_fraction=0.1),
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        scoring='accuracy',
        verbose=1
    )
    grid_search.fit(wdbc.data, wdbc.target)

    best_model = grid_search.best_estimator_
    cv_results = model_selection.cross_validate(
        best_model, wdbc.data, wdbc.target, cv=5, return_train_score=True
    )
    
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')