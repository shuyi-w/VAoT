# Author: Shuyi Wu
# Date: 17 October 2026
# Description: Selection of data

import pandas as pd
import numpy


#to create dictionary of data

df = pd.read_csv("VAoT_anon.csv")


"""Re-arrange dataframe"""
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

"""Date of Birth -> Age"""
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
    (merged_df["Surgery After 1st Injection"] != "Cataract") &
    (merged_df["Prior Cataract Surgery"] != 1) &
    (merged_df["Prior PPV Surgery"] != 1)
]

"""prints out df to csv file"""
cleaned_df.to_csv("VAoT_reorganised.csv")
