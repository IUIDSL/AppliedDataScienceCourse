
# coding: utf-8

# In[1]:

import seaborn as sns, pandas as pd, matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# The command: <code>%matplotlib inline</code> allows for inline display of plots; normally you have to do plt.show() to display your plots.
# 
# Check out matplotlib plots <code>savefig</code> method for saving plots to disk (especially usefull for including them in your reports!) You can find that here: https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.savefig.html

# In[4]:

df = pd.read_csv("C:/Users/Shahidhya/Downloads/low_birth_rate_full.csv")
df.columns = ["ID","LOW","AGE","LWT","RACE","SMOKE","PTL","HT","UI","FTV","BWT"]
df.info()


# low: indicator of birth weight less than 2.5kg
# age: mother's age in years
# lwt: mother's weight in pounds at last menstrual period
# race: mothers race ("white", "black", "other")
# smoke: smoking status during pregnancy
# ht: history of hypertension
# ui: presence of uterine irritability
# ftv: number of physician visits during the first trimester
# ptl: number of previous premature labours
# bwt: birth weight in grams

# The first thing we want to do is load our data and make sure everything loaded properly. From previous experience, I know that the headers are going to load weird, so I overwrite them first thing after reading the data. Then, I use the data frames <code>.info()</code> to check the headers are as I want them and the data types for each.
# 
# <h3>First plot: scatterplot with linear correlation</h3>
# The first thing I want to do is compare birth weight and age. I know older mothers have a harder time giving birth, so maybe there's a relationship there. To do that, I pass BWT as my Y variable and AGE as my X variable to seaborns <code>lmplot</code> method (linear model plot). Below, you'll notice that not only does it plot the points, axes, and regression line, it also plots an error field. Super handy!

# In[34]:

sns.set(style="ticks")
sns.lmplot(y='BWT',x='AGE',data=df)


# Let's also check out the impact how the weight of the mother effects the child, controlling for race. (I don't really have any hypotheses about this, I just want to show you how we can do this.)

# In[5]:

sns.lmplot(y="BWT",x="LWT",hue="RACE",data=df) #Remember, 1=white, 2=black, 3=other

# If I wanted to save this plot:
# p = sns.lmplot(y="BWT",x="LWT",hue="RACE",data=df) 
# p.savefig("fancy-regression-chart.png")


# <h3>Second plot: violin plots</h3>
# Violin plots are an excellent way to explore data. They work like t-tests -- but instead of having to interpret P and R-squared values, we look at the plots to guage the difference. This time, I want to see how the smoking status of the mother impacts the birthweight of the baby -- I suspect there may be something going on.

# In[35]:

sns.violinplot(y="BWT",x="SMOKE",data=df)


# It's a close one. There could be a significant difference between the two populatons, but also, maybe not. Let's see what happens when we add hypertension into the mix.

# In[38]:

sns.violinplot(y="BWT",x="HT",hue="SMOKE",data=df)


# <h3>Third Plot: Factorplot</h3> 
# We can also compare the interaction using bar charts.

# In[53]:

sns.factorplot(x="SMOKE",hue="LOW",col="HT",kind="count",data=df)


# <h3> Fourth plot: Correlation heat mep </h3>
# Used to analyze the correlation between all pairs of variables on a heatmap

# In[17]:

import numpy as np

corr = df.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


# <h3>Fifth Plot: Pairplots </h3>
# To understand the distribution of each variable and also plot it against all other variables to understand their relationship. The graph can be visualized for different values of a chosen 'hue' variable

# In[19]:

df1 = df[['AGE','LWT','BWT','FTV','PTL','LOW']]
sns.pairplot(df1, hue = 'LOW',size=2.5);


# <h3> Sixth Plot: Histogram with Kernel Density Estimate</h3>
# To understand the distribbution of a single variable, we plot the histogram and overlay the distribution of the variable. Helps identify skew in the data.

# In[27]:

sns.distplot(df['LWT'], bins = 20, rug = True)

