import pandas as pd

# Reading survey from XLSX
root = "G:\\Me\\Code\\UOC\\TFM\\demeter\\data\\survey\\"
inputs = root + "inputs\\"
outputs = root + "outputs\\"

file_name = inputs + "FAQ.xlsx"
xls = pd.ExcelFile(file_name) 
sheet = xls.parse("Form Responses 1")

#file_name = inputs + "FAQ.csv"
#sheet = pd.read_csv(file_name, encoding = 'ISO-8859-1')

sheet.columns = ["timestamp","country","age","social_network","profile","cultivars","places","forecast_precipitation","climatology","forecast_yield","forecast_date"]

# Spliting columns intents by comma
df = pd.DataFrame()
split_comma = lambda x: pd.Series([i for i in reversed(x.split(','))])
for c in ["cultivars","places","forecast_precipitation","climatology","forecast_yield","forecast_date"]:
    print ("Processing " + c)
    df2 = sheet[c].apply(split_comma)
    for c2 in df2.columns:     
        tmp = df2[c2]
        tmp = tmp.dropna()
        tmp = tmp.to_frame()
        tmp["intent"] = c
        tmp.columns = ["question","intent"]
        df = df.append(tmp, ignore_index=True)
        
print (df.head())
df.to_csv(outputs +'01-intents.csv', index = False, encoding='utf-8-sig')

# Cleaning records

def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trim_strings)

# replace all enters inside of the text
df2 = df.replace(r'\\n',' ', regex=True) 
df2 = df.replace(r'  ',' ', regex=True) 
# Remove blank spaces starting and ending inside of the text
df2 = trim_all_columns(df2)
# Remove quotes
df2["question"] = df2["question"].str.replace('"', '')
# Count number of words in each intent
df2["n_words"]  = df2['question'].str.split().str.len()
# Saving output
df2.to_csv(outputs +'02-intents.csv', index = False, encoding='utf-8-sig')

# Filtering data
df3 = df2.loc[df2["n_words"] > 2,:]
df3.to_csv(outputs +'03-intents.csv', index = False, encoding='utf-8-sig')

# Spliting columns each word by space
df4 = df3.loc[:,["question","intent"]]
df4['question'] = [':O '.join(x.split()) for x in df4['question']]
df4['question'] = df4['question'] + ":O"
print (df4.head())
df4.to_csv(outputs +'04-intents.csv', index = False, encoding='utf-8-sig')