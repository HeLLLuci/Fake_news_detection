from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import pickle
import pandas as pd 
from sklearn.model_selection import train_test_split

app = Flask(__name__)


tfvect = TfidfVectorizer(stop_words='english', max_df=0.7)
loaded_model = pickle.load(open('model.pkl', 'rb'))
df = pd.read_csv(r'D:/Its Me/Datasets/fake_or_real_news.csv')
x = df['text']
y = df['label']
x_train,x_test,y_train,y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


def model(news):
    tfid_x_train = tfvect.fit_transform(x_train)
    tfid_x_test = tfvect.transform(x_test)
    input_data = [news]
    vectrorized_input_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectrorized_input_data)
    return prediction


@app.route('/')    
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method =='POST':
        message = request.form['message']
        pred = model(message)
        print(pred)
        return render_template('index.html', prediction=pred)
    else:
        return render_template('index.html', prediction="Something went wrong")


if __name__ == '__main__':
    app.run(debug=True)   