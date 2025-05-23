# Data Science Salary Estimator
**The main purpose of making this project is learning. It is completely followed by using youtube tutorial of Ken Jee (link will be list below)**

---

## Project Overview 
* Created a tool that estimates data science salaries to help data scientists negotiate their income when they get a job.
* Using dowloaded dataset that contain over 3000 job descriptions from **Kaggle** (can not scrape from Glassdoor)
* Engineered features from the text of each job description to quantify the value companies put on python, excel, aws, and spark. 
* Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model. 
* Built a client facing API using flask 

---

## Code and Resources Used 
**Python Version:** 3.11  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
**Youtube Tutorial:** https://www.youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t  
**Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
**Kaggle dataset:** https://www.kaggle.com/datasets/andrewmvd/data-scientist-jobs  
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2  

---

## Dataset
Get the Data Scientist dataset from **Kaggle**. With each job, we got the following:
*	Job title
*	Salary Estimate
*	Job Description
*	Rating
*	Company 
*	Location
*	Company Headquarters 
*	Company Size
*	Company Founded Date
*	Type of Ownership 
*	Industry
*	Sector
*	Revenue
*	Competitors 

---

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

*	Parsed numeric data out of salary 
*	Made columns for employer provided salary and hourly wages 
*	Removed rows without salary 
*	Parsed rating out of company text 
*	Made a new column for company state 
*	Added a column for if the job was at the company’s headquarters 
*	Transformed founded date into age of company 
*	Made columns for if different skills were listed in the job description:
    * Python  
    * R  
    * Excel  
    * AWS  
    * Spark 
*	Column for simplified job title and Seniority 
*	Column for description length 

---

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables. 
*** Adding pics and write about it here

---

## Model Building 

First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.   

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.   

I tried three different models:
*	**Multiple Linear Regression** – Baseline for the model
*	**Lasso Regression** – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
*	**Random Forest** – Again, with the sparsity associated with the data, I thought that this would be a good fit. 

---

## Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets. 
*	**Random Forest** : MAE = 11.22
*	**Linear Regression**: MAE = 18.86
*	**Ridge Regression**: MAE = 19.67

---

## Productionization 
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary. 

---

# Learning Outcomes:
The learning outcomes that I gained after completed this Project.
## Soft and Collaborative skills

### Workflow
* Understand and follow the complete lifecycle of a data science project, including planning, data collection, exploration, modeling, evaluation, and deployment.
* Understand of what should be done in each steps and how to seeking for help, references.

### Github use 
* Understand how the GitHub can be included and be able to apply Git and GitHub to store and share the real project.

### Docomenting README.md
* Understand of using README.md to write clear and professional a explaination project goals, setup instructions, usage, and results.
* Shout out and list all the resources and references used in the project.

### Using VScode and Command Prompt
* Getting more familiar with VScode to code python.
* Using Command Prompt to manage files and directories.
---

## Technical Skills

### Data Collection
### Data Cleaning
### EDA
### Model Building
### FlaskAPI
