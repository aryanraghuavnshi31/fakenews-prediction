# -*- coding: utf-8 -*-
"""Fake News Detection using machine learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QOMvvLM4eoSFUiEp1V4ccJp5YNk3i2OM

# Fake News Detector

## Installing Necessary Libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

"""## Loading the data"""

data_fake = pd.read_csv('/content/Fake.csv', on_bad_lines='skip', encoding='utf-8')
data_true = pd.read_csv('/content/True.csv', on_bad_lines='skip', encoding='utf-8')

"""### Data Preview"""

data_fake.head()

data_true.tail()

data_fake["class"]=0
data_true['class']=1

data_fake.shape, data_true.shape

data_fake_manual_testing = data_fake.tail(10)
for i in range(23480,23470,-1):
    data_fake.drop([i],axis = 0, inplace = True)


data_true_manual_testing = data_true.tail(10)
for i in range(21416,21406,-1):
    data_true.drop([i],axis = 0, inplace = True)

data_fake.shape, data_true.shape

data_fake_manual_testing['class']=0
data_true_manual_testing['class']=1

data_fake_manual_testing.head(10)

data_true_manual_testing.head(10)

data_merge=pd.concat([data_fake, data_true], axis = 0)
data_merge.head(10)

"""#### "title",  "subject" and "date" columns is not required for detecting the fake news, so I am going to drop the columns."""

data_merge.columns

data=data_merge.drop(['title','subject','date'], axis = 1)

#count of missing values
data.isnull().sum()

"""#### Randomly shuffling the dataframe"""

data = data.sample(frac = 1)

data.head()

data.reset_index(inplace = True)
data.drop(['index'], axis = 1, inplace = True)

data.columns

data.head()

"""## Preprocessing Text

#### Creating a function to convert the text in lowercase, remove the extra space, special chr., ulr and links.
"""

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]','',text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+','',text)
    text = re.sub('<.*?>+',b'',text)
    text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
    text = re.sub('\w*\d\w*','',text)
    return text

data['text'] = data['text'].apply(wordopt)

"""#### Defining dependent and independent variable as x and y"""

x = data['text']
y = data['class']

"""## Training the model

#### Splitting the dataset into training set and testing set.
"""

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25)

"""### Extracting Features from the Text

#### Convert text to vectors
"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

"""## Logistic Regression"""

from sklearn.linear_model import LogisticRegression

LR = LogisticRegression()
LR.fit(xv_train, y_train)

pred_lr = LR.predict(xv_test)

LR.score(xv_test, y_test)

print (classification_report(y_test, pred_lr))

"""## Decision Tree Classifier"""

from sklearn.tree import DecisionTreeClassifier

DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)

pred_dt = DT.predict(xv_test)

DT.score(xv_test, y_test)

print (classification_report(y_test, pred_lr))

"""## Gradient Boost Classifier"""

from sklearn.ensemble import GradientBoostingClassifier

# Use smaller parameters for faster training
GB = GradientBoostingClassifier(
    random_state=0,
    n_estimators=100,  # Reduced from default 100
    max_depth=3,       # Shallower trees
    learning_rate=0.1, # Default
    subsample=0.8,     # Use 80% of samples per tree
    verbose=1         # Show progress
)

try:
    GB.fit(x_train, y_train)
except KeyboardInterrupt:
    print("Training interrupted - current progress saved")
    # Model will still be usable with whatever progress was made

pred_gb = GB.predict(xv_test)

GB.score(xv_test, y_test)

print(classification_report(y_test, pred_gb))

"""## Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(random_state = 0)
RF.fit(xv_train, y_train)

pred_rf = RF.predict(xv_test)

RF.score(xv_test, y_test)

print (classification_report(y_test, pred_rf))

"""## Testing the Model"""

def output_lable(n):
    if n==0:
        return "Fake News"
    elif n==1:
        return "Not A Fake News"

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GB = GB.predict(new_xv_test)
    pred_RF = RF.predict(new_xv_test)

    return print("\n\nLR Predicition: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction:{}".format(output_lable(pred_LR[0]),
                                                                                                             output_lable(pred_DT[0]),
                                                                                                             output_lable(pred_GB[0]),
                                                                                                             output_lable(pred_RF[0])))

"""### Model Testing With Manual Entry"""

news = str(input())
manual_testing(news)

news=str(input())
manual_testing(news)

