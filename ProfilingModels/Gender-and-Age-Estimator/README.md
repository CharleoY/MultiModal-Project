Age and Gender Estimator
--------------------
Client-server service, that predicts user age and gender. Client sends text messages to RabbitMQ, server(s) receive messages and predict age/gender and print result to console or save to file.


### File list

1. :file_folder: **Source**
	1. :page_facing_up: **client.py** - sending messages to RabbitMQ.
	2. :page_facing_up: **server.py** - receiving messages from RabbitMQ, load model from file, predict age/gender and print answer to console/save to output file.
	3. :page_facing_up: **input-data-handler.py** - prepocessing data for features calculation and building models
	4. :page_facing_up: **feature-extraction.py** - calculating features
	5. :page_facing_up: **Gender_Age_Models.ipynb** - building and fitting different models
2. :file_folder: **Resources**
	1. :file_folder: **data** - initial input data, **.xml** files with users tweets, used for feature calculation
	2. :file_folder: **dicts** - dictionary files for calculation features, such as most common ngrams, users texts corpuses and etc.
	3. :file_folder: **models** - different models that were fitted to predict age/gender
	4. :page_facing_up: **data.csv** - initial file with target variables and user ids
	5. :page_facing_up: **data_features.csv** - final file with calculated features
	6. :page_facing_up: **input.json** - file for input messages to predict user age/gender



### How to run
To run server(s) write the following command:
```
python server.py
```
Running servers are waiting for messages in **messages queue** in RabbitMQ, handling them if they appears, calculating features and predict age/gender. Results of predicting will be printed to console. If everything is correct, you will see the following:
```
[*] Waiting for messages. To exit press CTRL+C
[x] Received b'Such a good day! I will go shopping.'
[x] Age: "18-24", Gender: "MALE".
```
To send messages to server put them in **json**-format to file **input.json**. Example:
```
{
  "messages": [
      "Such a good day! I will go shopping.",
      "I really do not like this fashion show."
  ]
}
```
Then run the following command:
```
python client.py
```
If everything is correct you will see thw following:
```
[x] Sent 'Such a good day! I will go shopping.'
[x] Sent 'I really do not like this fashion show.'
```



### Features
The main resource to study what features are needed to predict age/gender was the PAN'16 winners article. Initial messages had some preprocessing, such as hashtags/urls/stop words deleting.

| Features         | Description                  |
 ----------------- | ---------------------------- |
| N-grams			| Number of most popular 1, 2 and 3-grams for every user           |
| Mentions          | Average number of mentions per message            |
| Punctuation         | Average number of punctuation per message            |
| Text size        | Average number of message size for user` |
| Starts with capital       | Average number of message, that starts with capital letter |
| Ends with punctuation        | Average number of message, that ends with punctuation |
| Capitals       | Average number of capital letter per message |
| Words count        | Average number of words per message |
| Vocabulary richness        | Percentage of unique words for user |
| POS tagging       | Average number of every part of speech per message |

### Models
To predict age/gender the following models were fitted:

1. Logistic Regression (sklearn)
2. Gradient Boosting Classifier (sklearn)
3. Support Vector Classifier (sklearn)
Initial data with features was preprocess using StandartScaler from sklearn library.
GridSearch was used to  find best parametrs for models.

####Models results
| Model         | Age Score                | Gender Score|
|---------------| -------------------------|  ---------- |
|Logistic Regression| 0.432|  **0.580** |
|Gradient Boosting| 0.420|  0.420 |
|Support Vector Classifier| **0.460**|  0.570 |
The best scores was for Logistic Regression in gender prediction and for Support Vector Classifier in age prediction.
