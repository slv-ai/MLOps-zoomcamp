
| Production | Key Questions|
|--------|-----|
| Data distribution changes | Why are there sudden changes in the values of my features?|
|Model ownership in production | Who owns the model in production? The DevOps team? Engineers? Data Scientists?|
|Training-serving skew|Why is the model giving poor results in production despite our rigorous testing and validation attempts during development?|
|Model/concept drift|Why was my model performing well in production and suddenly the performance dipped over time?|
|Black box models|How can I interpret and explain my model’s predictions in line with the business objective and to relevant stakeholders?|
|Concerted adversaries|How can I ensure the security of my model? Is my model being attacked?|
|Model readiness|How will I compare results from a newer version(s) of my model against the in-production version(s)?|
|Pipeline health issues|Why does my training pipeline fail when executed? Why does a retraining job take so long to run?|
|Underperforming system|Why is the latency of my predictive service very high? Why am I getting vastly varying latencies for my different models?|
|Cases of extreme events (outliers)|How will I be able to track the effect and performance of my model in extreme and unplanned situations?|
|Data quality issues|How can I ensure the production data is being processed in the same way as the training data was?|

So we have to:
- monitor model performance in production: see how accurate the predictions of your model are. See if the model performance decays over time, and you should re-train it.
- monitor model input/output distribution: see if the distribution of input data and features that go into the model changed? Has the predicted class distribution changed over time? Those things could be connected to the data and concept drift.
- monitor model training and re-training: see learning curves, trained model predictions distribution, or confusion matrix during training and re-training.
- monitor model evaluation and testing: log metrics, charts, prediction, and other metadata for your automated evaluation or testing pipelines
- monitor hardware metrics: see how much CPU/GPU or Memory your models use during training and inference.
- monitor CI/CD pipelines for ML: see the evaluations from your CI/CD pipeline jobs and compare them visually. In ML, the metrics often only tell you so much, and someone needs to actually see the results.

Ref: 
* [A Comprehensive Guide on How to Monitor Your Models in Production](https://neptune.ai/blog/how-to-monitor-your-models-in-production-guide)
* [Best Tools to Do ML Model Monitoring](https://neptune.ai/blog/ml-model-monitoring-best-tools)
### What is data drift

Data drift, or covariate shift, refers to the phenomenon where the distribution of data inputs that an ML model was trained on differs from the distribution of the data inputs that the model is applied to. This can result in the model becoming less accurate or effective at making predictions or decisions.

Ref: 
[Data Drift vs. Concept Drift: What Is the Difference?](https://www.dataversity.net/data-drift-vs-concept-drift-what-is-the-difference/#:~:text=Data%20drift%20refers%20to%20the,of%20a%20machine%20learning%20model.)
### How is machine learning monitoring different?
Main:
- Service Health
Monitored by few metrics, which is also a must since have to make sure the service works.
- Model Health
Check how good the service provided. Evaluation metrics are based on tasks, for example, searching/recommendation system requires ranking metrics; regression requires
MAE or MAP; classification requires Log loss, precision or recall.
- Data quality and integrity
Check catch for the data quality when receiving and generating outputs, metrics such as share or missing values or count time, value range for each kind.
- Data and concept drift
Check the distribution of input and output which may be effected by real-world environment 

Others:
- Performance by segments
Check the quality metrics by segments when diverse objects/categories
- Bias and fairness
- Outliers
- Explainability

### Monitoring types
Batch Monitoring:

Online (non-batch) Monitoring:

### What is monitoring scheme
- Use Service: Implement the service as REST API or batch pipeline.
- Obtain logs: Generate logs as local log file when using the service
- Calculate Metrics based on logs
- Load Metrics into a Database: save the calculated metrics into a PostgreSQL database.
- Build a Dashboard: Use Grafana to build a dashboard with the data from PostgreSQL database.
