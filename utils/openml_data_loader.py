import os
import openml
import pandas as pd

def download_and_save(
    save_path: str,
    suite_id_or_name=None,
    dataset_name_or_id=None,
    task_id=None,
):
    """Downloads OpenML data based on user input and saves it inside the compulsory save_path."""
    # Define and create features and targets directories inside the user's path
    X_path = os.path.join(save_path, "features")
    y_path = os.path.join(save_path, "targets")
    os.makedirs(X_path, exist_ok=True)
    os.makedirs(y_path, exist_ok=True)

    # FLOW 1: User provides a suite ID/name -> extracts all tasks and saves them
    if suite_id_or_name is not None:
        suite = openml.study.get_suite(suite_id_or_name)
        for t_id in suite.tasks:
            task = openml.tasks.get_task(t_id)
            dataset = task.get_dataset()
            # task.get_X_and_y returns exactly 2 items
            X, y = task.get_X_and_y(dataset_format="dataframe")

            X.to_csv(os.path.join(X_path, f"{dataset.name}_features.csv"), index=False)
            y.to_csv(os.path.join(y_path, f"{dataset.name}_target.csv"), index=False)

    # FLOW 2: User provides a single dataset name or dataset ID directly
    elif dataset_name_or_id is not None:
        dataset = openml.datasets.get_dataset(dataset_name_or_id)
        # dataset.get_data returns exactly 4 items
        X, y, _, _ = dataset.get_data(
            target=dataset.default_target_attribute, dataset_format="dataframe"
        )

        X.to_csv(os.path.join(X_path, f"{dataset.name}_features.csv"), index=False)
        y.to_csv(os.path.join(y_path, f"{dataset.name}_target.csv"), index=False)

    # FLOW 3: User provides a single specific task ID directly
    elif task_id is not None:
        task = openml.tasks.get_task(task_id)
        dataset = task.get_dataset()
        # task.get_X_and_y returns exactly 2 items
        X, y = task.get_X_and_y(dataset_format="dataframe")

        X.to_csv(os.path.join(X_path, f"{dataset.name}_features.csv"), index=False)
        y.to_csv(os.path.join(y_path, f"{dataset.name}_target.csv"), index=False)
