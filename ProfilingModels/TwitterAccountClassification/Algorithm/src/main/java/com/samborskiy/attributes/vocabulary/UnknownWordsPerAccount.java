package com.samborskiy.attributes.vocabulary;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Number of words not found in the dictionary, divided by the total number of tweets.
 *
 * @author Whiplash
 */
public class UnknownWordsPerAccount extends AttributeFunction {

    @Override
    public String getName() {
        return "unknown_word_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0.;
        for (String tweet : tweets) {
            for (String word : tweetParser.parse(tweet)) {
                if (morphologicalAnalyzer.get(word) == null) {
                    count++;
                }
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
