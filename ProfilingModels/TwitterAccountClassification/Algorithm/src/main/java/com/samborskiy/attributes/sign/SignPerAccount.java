package com.samborskiy.attributes.sign;

import com.samborskiy.entity.sequences.SignSequence;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * The number of appearances sign in tweets divided by the total number of tweets.
 */
public class SignPerAccount extends SignFunction {

    private final SignSequence sequence;

    public SignPerAccount(SignSequence sequence) {
        this.sequence = sequence;
    }

    @Override
    public String getName() {
        return String.format("%s_per_tweet", sequence.toString());
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (String tweet : tweets) {
            count += sequence.count(tweet);
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
