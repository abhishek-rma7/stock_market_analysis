import pandas as pd
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score, recall_score
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

df = pd.read_csv('Data.csv', encoding="ISO-8859-1")
df.dropna(inplace=True)

train = df[df['Date'] < '20150101']
test = df[df['Date'] > '20141231']
print('Train size: {}, Test size: {}'.format(train.shape, test.shape))

y_train = train['Label']
train = train.iloc[:, 3:28]
y_test = test['Label']
test = test.iloc[:, 3:28]

train.replace(to_replace='[^a-zA-Z]', value=' ', regex=True, inplace=True)
test.replace(to_replace='[^a-zA-Z]', value=' ', regex=True, inplace=True)

new_columns = [str(i) for i in range(0, 24)]
train.columns = new_columns
test.columns = new_columns

for i in new_columns:
    train[i] = train[i].str.lower()
    test[i] = test[i].str.lower()

train_headlines = []
test_headlines = []
for row in range(0, train.shape[0]):
    train_headlines.append(' '.join(str(x) for x in train.iloc[row, 0:25]))
for row in range(0, test.shape[0]):
    test_headlines.append(' '.join(str(x) for x in test.iloc[row, 0:25]))

ps = PorterStemmer()
train_corpus = []
for i in range(0, len(train_headlines)):
    words = train_headlines[i].split()
    words = [word for word in words if word not in set(stopwords.words('english'))]
    words = [ps.stem(word) for word in words]
    headline = ' '.join(words)
    train_corpus.append(headline)

test_corpus = []
for i in range(0, len(test_headlines)):
    words = test_headlines[i].split()
    words = [word for word in words if word not in set(stopwords.words('english'))]
    words = [ps.stem(word) for word in words]
    headline = ' '.join(words)
    test_corpus.append(headline)

cv = CountVectorizer(max_features=10000, ngram_range=(2, 2))
X_train = cv.fit_transform(train_corpus).toarray()
X_test = cv.transform(test_corpus).toarray()

lr_classifier = LogisticRegression()
lr_classifier.fit(X_train, y_train)

lr_y_pred = lr_classifier.predict(X_test)

rfc = RandomForestClassifier(n_estimators=200, criterion='entropy')
rfc.fit(X_train, y_train)
rfc_y_pred = rfc.predict(X_test)

score4 = accuracy_score(y_test, rfc_y_pred)
score5 = precision_score(y_test, rfc_y_pred)
score6 = recall_score(y_test, rfc_y_pred)
print("RFC - Accuracy score is: {}%".format(round(score4 * 100, 2)))
print("RFC - Precision score is: {}".format(round(score5, 2)))
print("RFC - Recall score is: {}".format(round(score6, 2)))

score1 = accuracy_score(y_test, lr_y_pred)
score2 = precision_score(y_test, lr_y_pred)
score3 = recall_score(y_test, lr_y_pred)
print("LR - Accuracy score is: {}%".format(round(score1 * 100, 2)))
print("LR - Precision score is: {}".format(round(score2, 2)))
print("LR - Recall score is: {}".format(round(score3, 2)))

joblib.dump(lr_classifier, 'stock_sentiment.pkl')

with open('countvector.pkl', 'wb') as f:
    pickle.dump(cv, f)
