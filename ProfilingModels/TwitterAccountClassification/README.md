# TwitterAccountClassification
Classification of Twitter accounts for individual (personal) and superindividual (corporate and character).

Library consist of two main modules: **Algorithm** and **DataExtraction**.

## Algorithm
Module is designed to classify types of Twitter accounts. Example of using this you can find in [Demo](https://github.com/Nilera/TwitterAccountClassification/blob/refactoring/Demo/src/main/java/com/samborskiy/demo/Classifier.java) module.

To modify module you can set *twitter_classifier.properties* file into project folder. The following is a list of parameters that can be specified in this file:

**debug** — boolean variable, if set, classifier is run in debug mode and may output additional info to the console 
(default: false)

**frequency_analyzer** — package of needed frequency analyzer (default: com.samborskiy.entity.analyzers.frequency.FrequencyDictionary)

**grammar_analyzer** — package of needed frequency analyzer (default: com.samborskiy.entity.analyzers.frequency.JLanguageToolGrammarCheckerRu)

**morphological_analyzer** — package of needed frequency analyzer (default: com.samborskiy.entity.analyzers.frequency.SimpleMorphologicalAnalyzer)

**sentence_analyzer** — package of needed frequency analyzer (default: com.samborskiy.entity.analyzers.frequency.SimpleTweetParser)

**attributes** — path to file with attributes names which will be used to classify (default: res/random_forest_attributes)

## DataExtraction
Support module to sampling. To begin to use this you should to set [*twitter4j.properties*](http://twitter4j.org/en/configuration.html) file into project folder. 

Also you need to create configuration file the following form ([example](https://github.com/Nilera/TwitterAccountClassification/blob/refactoring/res/ru/config.json)):
```
{
  "lang": String, language of sample (example: "ru"),
  "databasePath": String, path to database file (example: "res/ru/test.db"),
  "types": array of Type, type of accounts
}
```

Type:
```
{
  "id": int, class id using to classify (example: 0),
  "name": String, human readable identify of type (example: "personal"),
  "tweetPerUser": int, number of tweet which will be download per user (example: 500),
  "data": Data, list of screen names of user ids which will be download
}
```

Data:
```
{
  "screenNames": String, path to file with list of screen names to download (example: "res/ru/screen_names_0")
  or
  "userIds": String, path to file with list of user ids to download (example: "res/ru/user_ids_0")
}
```
