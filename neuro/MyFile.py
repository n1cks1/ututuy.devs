import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

my_set = pd.read_csv('public_data.csv', index_col= 0)
my_set = my_set

# print(my_set.columns)

unique_classes = my_set.iloc[:, 1].unique()

selected_classes = ["Hardware", "Access", "Miscellaneous", "HR Support", "Purchase", "Administrative rights", "Storage", "Internal Project"]
df_selected = my_set[my_set["Topic_group"].isin(selected_classes)]


my_set_imb = my_set[my_set["Topic_group"].isin(selected_classes)]

X = my_set_imb.drop(columns=["Topic_group"])
y = my_set_imb["Topic_group"]

rus = RandomUnderSampler(random_state= 0)
X_resampled, y_resampled = rus.fit_resample(X, y)

topics = {topic: i for i, topic in enumerate(unique_classes)}
tokenized = [topics[topic] for topic in y_resampled]

my_set_balanced = pd.DataFrame(X_resampled)
my_set_balanced["Topic_group"] = tokenized

train, test = train_test_split(my_set_balanced, test_size=0.33, random_state=42)

train_x, train_y = train["Document"], train["Topic_group"]
test_x, test_y = test["Document"], test["Topic_group"]

tfidf = TfidfVectorizer(stop_words='english')

train_x_vector = tfidf.fit_transform(train_x)

test_x_vector = tfidf.transform(test_x)

logreg = LogisticRegression(max_iter=2000).fit(train_x_vector, train_y)


print(logreg.score(test_x_vector, test_y))

