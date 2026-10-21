# Author: Shuyi Wu
# Date: 21 October 2026
# Description: Selection of data

import pandas as pd
import numpy
import random

"""to pseudonymisation data"""

df = pd.read_csv("VAoT.csv")

def randomise(n):
    rng = random.Random(str(n))
    return rng.randint(1, len(df))

df["Hospital Number"] = [randomise(n) for n in df["Hospital Number"]]
df["NHS Number"] = [randomise(n) for n in df["NHS Number"]]
df["Responsible Clinician at 1st Injection"] = [randomise(n) for n in df["Responsible Clinician at 1st Injection"]]
df["Hospital of 1st Injection"] = [randomise(n) for n in df["Hospital of 1st Injection"]]

"""re-arrange csv into dataframe"""
#(patient and location characteristics) age, sex, ethnicity, responsible clinician, hospital location, L/R eye, both eyes?, indication, date of 1st injection, drug used,
#(follow-up): no. of visits, follow up interval, delay in days,
#(variables prior): diabetic, cataract, glaucoma/glaucoma surgery, RD, PPV, intraretinal fluid, sub retinal fluid, intraretinal haemorrhage, subretinal haemorrhage,
#(complications after 1st injection): endophthalmitis, uveitis, retinal detachment, surgery post injection,
#(outcomes): baseline VA, change from baseline per visit   

df = df[['Hospital Number', 'NHS Number', 'Date of Birth', 'Gender', 'Ethnicity', 'Responsible Clinician at 1st Injection', 'Hospital of 1st Injection', 'Eye', 'Fellow Eye Treated', 'Date of 1st Injection', 'Drug at 1st Injection',
         'Number of Prior Recorded Anti-VEGF Injections', 'Follow-Up Interval', 'Days From Centre of Interval',
         'Current Diabetic Status', 'Prior Cataract Surgery', 'Prior Glaucoma', 'Prior Glaucoma Surgery', 'Prior RD Surgery', 'Prior PPV Surgery', 'Prior Intraretinal Fluid', 'Prior Subretinal Fluid', 'Prior Intraretinal Haemorrhage', 'Prior Subretinal Haemorrhage', 
         'Endophthalmitis After First Injection', 'Uveitis After First Injection', 'Retinal Detachment After First Injection', "Surgery After 1st Injection", 
         'Baseline VA Date', 'Baseline VA Letter Score', 'VA Date', 'VA Letter Score']]


#"""DoB -> Age"""

#df["Date of Birth"] = pd.to_datetime(df["Date of Birth"])
#today = pd.Timestamp.today()
#df["Age"] = (
#    today.year - df["Date of Birth"].dt.year
#    - (
#        (today.month, today.day)
#        < (df["Date of Birth"].dt.month, df["Date of Birth"].dt.day)
#    )
#)

def combine(x):
    values = x.dropna().unique()
    return values[0] if len(values) == 1 else list(values)

merged_df = (df.groupby(['Hospital Number', 'NHS Number'], as_index = False)
             .agg(combine))

"""remove pts w/ recorded cataract and PPV"""

cleaned_df = merged_df[
    #(merged_df[~merged_df["Surgery After 1st Injection"].str.contains('Cataract', na = False)]) &
    (merged_df["Prior Cataract Surgery"] != 1) &
    (merged_df["Prior PPV Surgery"] != 1)
]

#drop Prior Cataract and Prior PPV columns
cleaned_df = cleaned_df.drop(['Prior Cataract Surgery', 'Prior PPV Surgery'], axis=1)

"""prints out df to csv file"""
cleaned_df.to_csv("VAoT_reorganised.csv")
