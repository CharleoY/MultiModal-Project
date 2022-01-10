package com.samborskiy.attributes.frequency;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Average frequency of words in a tweet, divided by the number per tweet.
 *
 * @author Whiplash
 */
public class FrecuencyPerAccount extends AttributeFunction {

    @Override
    public String getName() {
        return "frequency_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double frequency = 0.;
        for (String tweet : tweets) {
            double tweetFrequency = 0.;
            List<String> words = tweetParser.parse(tweet);
            for (String word : words) {
                tweetFrequency += frequencyAnalyzer.getFrequency(word);
            }
            frequency += tweetFrequency / words.size();
        }
        attributes.add(new Attribute(frequency, getName()));
    }
}
