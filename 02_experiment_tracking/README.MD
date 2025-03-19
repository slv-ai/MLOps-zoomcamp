## MLflow

### What is MLflow?
MLflow is *"An open source platform for the machine learning lifecycle"*

In reality it's just a pip-installable Python package that contains four modules:
* `Tracking`: Focused on experiment tracking. 

    *"The MLflow Tracking is an API and UI for logging parameters, code versions, metrics, and output files when running your machine learning code and for later visualizing the results."* This can work beyond python, it works with REST, R, and Java APIs.
* `Models`: Types of models.

    *"An MLflow Model is a standard format for packaging machine learning models that can be used in a variety of downstream tools".*
* `Model Registry`: Used to manage models. 

    *"The MLflow Model Registry component is a centralized model store, set of APIs, and UI, to collaboratively manage the full lifecycle of an MLflow Model."*
* `Projects`: 
    *"An MLflow Project is a format for packaging data science code in a reusable and reproducible way, based primarily on conventions".* 


### MLflow tracking
MLflow tracking organises your experiment into *runs*. These runs keep track of: 
* `Parameters`: Alongside your typical input arguments etc. This can even include the path to the data you used to train/test the model, allowing you to even keep track of different preprocessing that you performed on the data
* `Scoring metrics`: Accuracy, F1 score, etc. metrics from train, test, and validation set
* `Metadata`: You can add tags to help you filter.
* `Artifacts`: Whatever outputs you deem necessary. Could even include figures, but this does come with a memory cost.
* `Models`: Sometimes it might even make sense to save the model. Especially if you are doing more than simple hyperparameter tuning.

Furthermore is also automatically logs metadata about the run including
* `Source code`
* `Version` (git commit),
* `Start` and `End` time
* `Author`

### Why is experiment tacking important?
* Reproducibility
* Organisation: Multiple people need to use the code or work on it so 
* Optimisation
This can all be run through a simple line

    $mlflow ui

NB There are some extra things you might need in the backend e.g. PostgresSQL.

## 2.2 Getting started with MLflow
This will be a brief description on how to use MLflow for an example problem

1. Create the venv
    ```
    $conda create -n environment_name
    ```
2. Activate the venv
    ```
    $conda activate environment_name
    ```
3. Install packages from the `requirements.txt`
    ```
    pip install -r requirements.txt

#### 2.2.3.2 Why Configure the Backend?
However, it might be necessary to hook-up a backend for several reasons.
* **Centralised Tracking**: By default MLflow stores metadata in local files. Making it hard to collaborate across a team, and also it could fill your memory with lots of files.

* **Model Registry**: The MLflow Model Registry requires a database-backed backend. That means if you want model versioning, annotations and/or lifecycle management. You need to configure a backend.

* **Scalability**: As discussed in the centralised tracking section local file storage can be inefficient as the number of runs increases. If you set up a database backend like MySQL, PostgreSQL, or SQLite you can scale up quickly and also query large amounts of data.

* **Persistence**: Local file storage can become inefficient and can be lost if the machine is restarted and/or files are deleted. The DB in the backend ensures run data persists and can be accessed reliably.

* **Remote Access**: If you configure the backend, you can store the run on the [MLflow tracking server](https://mlflow.org/docs/latest/tracking/server.html) which provides a centralised endpoint for accessing run data and artifacts remotely.

##### Creating a SQLite DB Backend
    Where the `--backend-store-uri` is the unique resoure identifier for your database. For example to create a local SQLite database:

    mlflow server --backend-store-uri sqlite:///mlflow.db

    the terminal should output a port that it is listening at. Copy and paste the port address (127.0.0.1:5000)into your browser and you should see the MLflow frontend.

### Storing Artifacts
    
    $mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

In this case the artifacts will be stored locally in a folder in the current working directory called `artifacts`. However there is also support to upload these artifacts to S3 buckets, GoogleCloud, and Azure Blobs. You can reac more on this in the [artifact documentation](https://mlflow.org/docs/latest/tracking/artifacts-stores.html) page.

### 2.2.4 Running MLflow in a jupyter notebook
1.Open the notebook you want to use \
2.Configure mlflow to begin tracking
    ```
    import mlflow

    mlflow.set_tracking_uri("sqlite:///mlflow.db") #The name of the database to use
    mlflow.set_experiment("new_experiment") #If already exists mlflow will append to existing data. Else it will make a new experiment
3.To track with mlflow
    ith mlflow.start_run():
        #MLflow tags
        mlflow.set_tag("developer","Marcus")
        mlflow.log_param("train-data-path",train_path)
        mlflow.log_param("val-data-path",val_path)

        #Model init
        params = {
            'max_depth': 15,
            'n_estimators': 50,
            'min_samples_split': 2,
            'min_samples_leaf': 4,
            'random_state': 42
        }
        #Store Random Forest Parameters
        mlflow.log_params(params)

        #Actually train the model
        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        #Evaluation
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse",rmse)
3.xgboost - Hyperparameter optimization with mlflow and select the best model
** HyperOpt:
Hyperopt has been designed to accommodate Bayesian optimization algorithms based on Gaussian processes and regression trees.
    from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
    
    from hyperopt.pyll import scope
* `f_min`: This function tries to find the minimum output.
* `tpe`: Tree-structured Parzen Estimator (TPE) function.
* `hp`: Library containing different methods to define the search space.
`STATUS_OK`: So we can print outputs at the end of each run.
`Trials`: To keep track of information for each run
* `pyll.scope`: used to define the range


search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 100, 1)),
        'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 20, 1)),
        'criterion' : hp.choice('criterion', ['squared_error', 'poisson']),
        'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 10, 1)),
        'random_state': 42
    }

*`hp.quniform` generates uniformly distributed values between a `min` and a `max` and the final value being the interval. This is similar for `hp.loguniform` which is for log distribution*
## 2.4 Model Management (Saving and Loading Models with MLflow)
The first version will usually get tested and then further changes will need to be made to improve it. In some cases we may even need to revert back to previous forms of the model.
    1.  MLflow log_artifact
 mlflow.log_artifact(local_path = "path/to/model.bin", artifact_path = "folder/for/models/)

When you go back to the MLflow UI and click on the run. in the artifacts section you should see a folder containing the model
    2.3 MLflow log_model()
        mlflow.xgboost.log_model(booster, artifact_path=./path/to/artifact/)

         mlflow.sklearn.log_model()
    2.4 Making predictions with the model.
         xgb_model = mlflow.xgboost.load_model(model_URI)

