#%%
import pandas as pd
#%%
# Read csv
df = pd.read_csv(r'C:\Users\Admin1\Documents\ds_salary_proj\DataScientist.csv')
print(df)
#%%
# parsing of job description

# %%
# salary parsing
# Clean the Salary Estimate attribute
df = df[df['Salary Estimate'] != '-1'] # remove all the -1 variable
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) # remove the (Glassdoor.est)
minus_K = salary.apply(lambda X: X.replace('K','').replace('$','')) # remove '$' and 'K' 
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0) # mark to identify if pay yearly or hourly

min_hr = minus_K.apply(lambda x: x.lower().replace('per hour',''))

# min salary
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
# max salary
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
# avr salary
df['AVR_salary'] = (df['min salary'] + df['max salary'])/2
# %%
# company name text only
df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)

# %%
# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()# To see how many job in a state
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1) # identify if location same as headquarter

# %%
# age of company
df['age'] = df.Founded.apply(lambda x: x if x < 1 else 2025 - x)
# %%
# parsing of job description
# python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# R Studio
df['RStudio_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
# Spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
# aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
# excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

# %%
# drop the Unname: 0
df_out = df.drop(['Unnamed: 0'], axis=1)

# %%
# export to CSV file
df_out.to_csv('Salary_data_cleaned.csv', index=0)
