import pandas as pd
import sklearn.neighbors._base # this is from `scikit-learn` instead of `sklearn`
import sys
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest

#from sklearn.experimental import enable_iterative_imputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.impute import IterativeImputer, SimpleImputer
#from sklearn.preprocessing import StandardScaler



data = pd.read_csv("combined_data.csv")

#separating features and target
X = data.drop(columns=["Action","Frame", "Video ID"])  #dropping non-feature columns
y = data["Action"]


#imputer = IterativeImputer(random_state=1)
#X_imputed = imputer.fit_transform(X)

imputer = MissForest()
X_imputed = imputer.fit_transform(X)

#normalizing might not be needed
#scaler = StandardScaler()
#X_scaled = scaler.fit_transform(X_imputed)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=1, stratify=y)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=200, random_state=1)
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

#feature importance
importances = clf.feature_importances_
feature_names = data.columns[1:-2]  #Excludes "Action", "Frame", "Video ID"
importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
importance_df.sort_values(by="Importance", ascending=False, inplace=True)

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x="Importance", y="Feature", data=importance_df)
plt.title("Feature Importance")
plt.show()
