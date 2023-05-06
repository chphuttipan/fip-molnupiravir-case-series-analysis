# 1. Import Python libraries 
from scipy.stats import shapiro 
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon
import pandas as pd
import matplotlib.pyplot as plt

# 2. Import CSV files from google colab 
from google.colab import files
uploaded = files.upload()
df = pd.read_csv("mu_fip_project_stat.csv")

# 3. Data cleaning
# 3.1 Replace 'na' (string) feature in each column by NaN (missing value)
df.loc[:, 'wbc':'ind_bili'] = df.loc[:, 'wbc':'ind_bili'].replace('na', pd.np.nan)
df.loc[:, 'alb_fluid':'ag_fluid'] = df.loc[:, 'alb_fluid':'ag_fluid'].replace('na', pd.np.nan)
df[['dose_monu','bw']] = df[['dose_monu', 'bw']].replace('na', pd.np.nan)

# 3.2 Set feature type in column as numeric data 
df.loc[:, 'wbc':'ind_bili'] = df.loc[:, 'wbc':'ind_bili'].apply(pd.to_numeric)
df.loc[:, 'alb_fluid':'ag_fluid'] = df.loc[:, 'alb_fluid':'ag_fluid'].apply(pd.to_numeric) 
df[['dose_monu','bw']] = df[['dose_monu', 'bw']].apply(pd.to_numeric)

# 3.3 Create column 'gb_fluid' from column 'tp_fluid' subtract by 'alb_fluid' 
df["gb_fluid"] = df["tp_fluid"] - df["alb_fluid"]

# 3.4 Create new table by filter data by column 'week' in DataFrame
df_w0 = df[df["week"] == 0]
df_w1 = df[df["week"] == 1]
df_w3 = df.loc[(df["week"] == 3) | (df["week"] == 4)]
df_w3.head()

# 3.5 Drop NaN (missing value) feature by row 
alb_f_w0 = df_w0["alb_fluid"].dropna() 
alb_f_w0

# 4. Create statistics functions
def shapiro_test(data):
  stat, p = shapiro(data)
  print('Test statistics:', stat)
  print('p-value:', p)
  
def pair_ttest(data1, data2):
  stat, p = ttest_rel(data1, data2)
  print('Test statistics:', stat)
  print('p-value:', p)  
  
def wilcoxon_test(data1, data2):
  stat, p = wilcoxon(data1, data2)
  print('Test statistics:', stat)
  print('p-value:', p)

# 5. Explain descriptive statistics by .describe()
sum_alb_f_w0 = alb_f_w0.describe()
print(sun_alb_f_w0)

# 6. Statistics A-B testing (Wilcoxon sign-ranked test and Pair T-test)
# 6.1 Preparing data before statistics testing
df_alt = pd.merge(df_w0[['number', 'alt']], df_w1[['number', 'alt']], on = 'number').merge(df_w3[['number', 'alt']], on = 'number')
df_alt = df_alt.rename(columns = {'alt_x': 'alt0', 'alt_y': 'alt1', 'alt' : 'alt3'})
df_alt = df_alt.dropna()
df_alt

# 6.2 Shapiro-Wilk test (data distribution test)
shapiro_test(df_alt['alt0'])

# 6.3 Wilcoxon sign-ranked test for non-normal distribution data
wilcoxon_test(df_alt['alt0'], df_alt['alt1'])

# 6.4 Pair T-test for normal distribution data
pair_ttest(df_alt['alt0'], df_alt['alt1'])

# 7. Create boxplot chart compare data in each weeks
fig, ax = plt.subplots()
ax.boxplot([df_alt['alt0'], df_alt['alt1'], df_alt['alt3']])

ax.set_title('Boxplot of Alanine Aminotranferase')
ax.set_xticklabels(['week 0', 'week 1', 'week 3'])
ax.set_ylabel('mg/dL')

plt.show()

