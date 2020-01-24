import os

from sklearn.base import is_classifier
from sklearn.utils import _safe_indexing

from ..utils.importing import import_module_from_source


class SKLearnPipeline(object):
    """Wrapper to convert a scikit-learn estimator into a RAMP workflow.

    Parameters
    ----------
    filename : str, default='estimator.py'
        The name of the python file used in the kit submission. In general,
        `estimator.py` is the used in RAMP starting-kit.
    """
    def __init__(self, filename='estimator.py'):
        self.filename = filename

    def train_submission(self, module_path, X, y, train_idx=None):
        """Train the estimator of a given submission.

        Parameters
        ----------
        module_path : str
            The path to the submission where `filename` is located.
        X : {array-like, sparse matrix, dataframe} of shape \
                (n_samples, n_features)
            The data matrix.
        y : array-like of shape (n_samples,)
            The target vector.
        train_idx : array-like of shape (n_training_samples,), default=None
            The training indices. By default, the full dataset will be used
            to train the model. If an array is provided, `X` and `y` will be
            subsampled using these indices.

        Returns
        -------
        estimator : estimator object
            The scikit-learn fitted on (`X`, `y`).
        """
        train_idx = slice(None, None, None) if train_idx is None else train_idx
        submission_module = import_module_from_source(
            os.path.join(module_path, self.filename),
            os.path.splitext(self.filename)[0]  # keep the module name only
        )
        estimator = submission_module.get_estimator()
        X_train = _safe_indexing(X, train_idx)
        y_train = _safe_indexing(y, train_idx)
        return estimator.fit(X_train, y_train)

    def test_submission(self, estimator_fitted, X):
        """Predict using a fitted estimator.

        Parameters
        ----------
        estimator_fitted : estimator object
            A fitted scikit-learn estimator.
        X : {array-like, sparse matrix, dataframe} of shape \
                (n_samples, n_features)
            The test data set.

        Returns
        -------
        pred : ndarray of shape (n_samples, n_classes) or (n_samples)
        """
        if is_classifier(estimator_fitted):
            return estimator_fitted.predict_proba(X)
        return estimator_fitted.predict(X)
