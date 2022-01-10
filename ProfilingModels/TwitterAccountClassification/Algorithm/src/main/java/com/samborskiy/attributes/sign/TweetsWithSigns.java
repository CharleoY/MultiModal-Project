package com.samborskiy.attributes.sign;

import com.samborskiy.entity.sequences.SignSequence;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * The number of tweets where is find any sign divided by the total number of tweets.
 */
public class TweetsWithSigns extends SignFunction {

    @Override
    public String getName() {
        return "tweets_with_signs";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (String tweet : tweets) {
            for (SignSequence sequence : SIGNS) {
                if (sequence.contains(tweet)) {
                    count++;
                    break;
                }
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
