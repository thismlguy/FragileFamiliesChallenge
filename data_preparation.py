
# coding: utf-8

# # Data Preparation Notebook
# This noteobook is part 1 of the code to generate the data which will go into the analysis done in R notebooks. This code requires the following to run:
# 
# * Python 3 environment
# * 2 Data Files present in a folder called FFChallenge:
#     - background.csv
#     - train.csv
# 
# Note: The data has been shared with privacy agreement so we can't share the dataset with you. You'll have to request access on your own.

# ## Load Data

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
get_ipython().magic('matplotlib inline')


# In[2]:

data = pd.read_csv('FFChallenge/background.csv')
outcomes = pd.read_csv('FFChallenge/train.csv')


# In[3]:

data.shape


# In[4]:

outcomes.shape


# In[5]:

#define the columns required and reduce the dataframe
required_cols = ['challengeID']
required_cols.extend(['cm%dcohp'%i for i in range(2,6)])
required_cols.extend(['cm%dmarp'%i for i in range(2,6)])
required_cols.extend(['m1e1b%d'%i for i in range(1,9)])
required_cols.extend(['cm%dcohf'%i for i in range(1,6)])
required_cols.extend(['m4a13','m5d2h','m4e2h','m2e2','m4c1c','m5a101'])
required_cols.extend(['cm%drelf'%i for i in range(1,6)])
required_cols.extend(['m%dc2'%i for i in range(2,5)]+['m5b2'])
required_cols.extend(['m%dc5'%i for i in range(2,5)]+['m5b3'])
required_cols.extend(['cm1edu','cf1edu','cm5md_case_con','cm5md_case_lib',
                      'cm3gad_case','cm3alc_case','cm3drug_case'])
required_cols.extend(['cm%dhhinc'%i for i in range(1,6)])
required_cols.extend(['k5b2d','k5b1d','k5b3d'])


# In[6]:

df = data[required_cols]
df.shape


# In[7]:

df = df.merge(outcomes[['challengeID','gpa','grit']],on='challengeID',how='left')
df.shape


# ## Drop rows

# ### drop values withouth gpa or grit

# In[8]:

df = df.dropna(subset=['gpa','grit'])


# In[9]:

df.shape


# ### not in wave
# use cohf for mothers not in wave

# In[10]:

cols = ['cm%dcohf'%i for i in range(1,6)]
df['num_mothers_not_in_wave'] = df[cols].apply(lambda x: sum(x==-9),axis=1)


# In[11]:

df['num_mothers_not_in_wave'].value_counts()


# In[12]:

#drop all:
df.loc[df['num_mothers_not_in_wave']!=0,'num_mothers_not_in_wave']=np.nan
df=df.dropna(subset=['num_mothers_not_in_wave'])
df.shape


# ### drop father custody:

# In[13]:

df['m4c1c'].value_counts()


# In[14]:

df.loc[df['m4c1c']==1,'m4c1c']=np.nan
df=df.dropna(subset=['m4c1c'])
df.shape


# In[15]:

df.head()


# # Features:

# In[16]:

#function for raw features
def view_var(data,x,year=[1,2,3,4],print_counts=False):
    col = []
    for t in x:
        col.extend([i for i in data.columns if t in i])
    print('cols found: %s'%col)
    if not print_counts:
        print(data[col].head(50))
    else:
        for x in col:
#             print('value counts for variable %s'%col)
            print(data[x].value_counts())


# In[17]:

def recode_vars(x,code_dict):
    d = {}
    for key,values in code_dict.items():
        for val in values:
            d[val]=key
    
    x2 = x.replace(d)
    assert set(np.unique(x2)) == set(code_dict.keys())
    return x2


# In[18]:

df_new = df.copy()


# ## Father's Involvement:

# In[19]:

#dictionary:
code_dict = {
    'full': [1],
    'partial': [2,3],
    'none': [4,5,-2,-6]
}

#cols:
cols = ['m%dc5'%i for i in range(2,5)]+['m5b3']
df_new[cols] = df[cols].apply(lambda x: recode_vars(x,code_dict=code_dict))


# In[20]:

#get score:
def involvement(x):
    key = {'full':5, 'partial':2.5, 'none':0}
    weights = [0.1, 0.2, 0.3, 0.4]
    absscore = [key[i] for i in x]
    weighted_score = np.dot(weights,absscore)
    return 'low' if weighted_score<1.75 else 'medium' if weighted_score<3.5 else 'high'


# In[21]:

# df_new[cols[1:]].apply(lambda x: ' '.join(x.values),axis=1).value_counts()


# In[22]:

df_new['father_involvement'] = df_new[cols].apply(involvement, axis=1)


# In[23]:

df_new['father_involvement'].value_counts()


# In[24]:

#test code
# x=range(0,6)

# for i in x:
#     print(i,'none' if i<2 else 'partial' if i<4 else 'full')


# ## Father's presence

# In[25]:

filter_cols = ['m%dc2'%i for i in range(2,5)]+['m5b2']
relf_cols = ['cm%drelf'%i for i in range(2,6)]
[i for i in zip(filter_cols,relf_cols)]


# In[26]:

for col in filter_cols:
    print(df[col].value_counts())


# m2c2: 0=dont know of child; 1=yes; 2=no; -2: dont know; -1: refused
# m3c2/m4c2/m5b2: 3=dont know of child; 1=yes; 2=no; -2: dont know; -1: refused

# In[27]:

def father_presence(df,df2,col,var):
    df2[col] = [np.nan]*df2.shape[0]
    print(col)
    df2.loc[[ x in [0,2,3] for x in df[var[0]] ],col] = 'none'
    df2.loc[[x in [1,2] for x in df[var[1]]],col] = 'full'
    df2[col]=df2[col].fillna('partial')
#     print(df2[col])


# In[28]:

df_new.shape


# In[29]:

new_cols = ['presence_%d'%i for i in range(2,6)]
for var in zip(filter_cols,relf_cols, new_cols):
    father_presence(df_new,df_new,var[2],var[:-1])


# In[30]:

for col in new_cols:
    print(df_new[col].value_counts())


# In[31]:

df_new[new_cols].head()


# In[32]:

df_new['father_presence'] = df_new[new_cols].apply(involvement, axis=1)


# In[33]:

df_new['father_presence'].value_counts()


# In[34]:

# df_new[new_cols].apply(lambda x: ' '.join(x.values),axis=1).value_counts()


# ## Number of partners
# apart from father

# In[35]:

cols = ['m4a13','m5a101']
for col in cols:
    print(df_new[col].value_counts())


# -10: only father -> 0
# -6: skipped -> 0
# -1: refused -> 0
# -2: dont know -> 0

# In[36]:

code_dict = {
    -6:0, -10:0, -1:0, -2:0
}
df_new['num_partners'] = df_new['m4a13'].replace(code_dict) + df_new['m5a101'].replace(code_dict)


# In[37]:

df_new['num_partners'].value_counts()


# ## Cohabitating with biological father

# In[38]:

relf_cols = ['cm%drelf'%i for i in range(2,6)]


# In[39]:

df_new['num_cohab_biof'] = df_new[relf_cols].apply( lambda x: sum([i in [1,2] for i in x]) ,axis=1)


# In[40]:

df_new['num_cohab_biof'].value_counts()


# ## Cohbitating with any partner

# In[41]:

cols = ['cm%dcohp'%i for i in range(2,6)]+['cm%dmarp'%i for i in range(2,6)]


# In[42]:

for col in cols:
    print(df_new[col].value_counts())


# In[43]:

df_new['cm2cohp']=df_new['cm2cohp'].replace({-3:0})


# In[44]:

df_new['num_cohab_anyp'] = df_new['num_cohab_biof'] + df_new[cols].apply( sum ,axis=1 )
df_new['num_cohab_anyp'] = [min(x,4) for x in df_new['num_cohab_anyp']]


# In[45]:

df_new['num_cohab_anyp'].value_counts()


# ## Control variables:

# ### education

# In[46]:

df_new['cm1edu'].value_counts()


# 1= <high school, 2: highschool; 3: some college/tech; 4: college/grad

# In[47]:

df_new['mothers_education'] = df_new['cm1edu']
df_new['fathers_education'] = df_new['cf1edu']


# In[48]:

df_new['fathers_education'].value_counts()


# In[49]:

#impute with 2:
df_new['fathers_education'] = df_new['fathers_education'].replace({-3:2})


# ### cidi

# In[50]:

cols = ['cm5md_case_con','cm5md_case_lib',
                      'cm3gad_case','cm3alc_case','cm3drug_case']
df_new['num_cidi_cases'] = df_new[cols].apply(lambda x: sum(x==1),axis=1)


# In[51]:

df_new['num_cidi_cases'].value_counts()


# In[52]:

# for col in cols:
#     print(df_new[col].value_counts())


# ### income:

# In[53]:

cols = ['cm%dhhinc'%i for i in range(1,6)]
df_new[cols].describe()


# In[54]:

df_new['hh_income'] = df_new[cols].apply(lambda x: np.log(np.mean(x)+1+1e-10),axis=1)
df_new['hh_income'].hist(bins=20)


# ### domestic spanking

# In[55]:

cols = ['k5b2d','k5b1d','k5b3d']
for col in cols:
    print(df_new[col].value_counts())


# In[56]:

code_dict={-6:0, -9:1, -1:1,-2:1,-3:1}
df_new['kid_punished'] = df_new[cols].apply(lambda x: sum(x.replace(code_dict)),axis=1)
df_new['kid_punished'].value_counts()


# ## Final exports:
# New features created:
# 
# Explanatory:
# * father_involvement
# * father_presence
# * num_partners
# * num_cohab_biof
# * num_cohab_anyp
# 
# Control:
# * mothers_education
# * fathers_education
# * num_cidi_cases
# * hh_income
# * kid_punished

# In[57]:

df_new.to_csv('FFChallenge/final_data.csv',index=False)

