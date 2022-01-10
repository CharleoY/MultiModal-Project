package com.samborskiy.attributes.sign;

import com.samborskiy.entity.sequences.SignSequence;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * The number of appearances of any sign divided by the total number of tweets.
 */
public class SignsPerAccount extends SignFunction {

    @Override
    public String getName() {
        return "signs_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (SignSequence sequence : SIGNS) {
            for (String tweet : tweets) {
                count += sequence.count(tweet);
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
