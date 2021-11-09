
import pandas as pd



df = pd.read_csv('output.csv')


print(df.to_string()) 
print(df.info())
print(df.loc[0])


