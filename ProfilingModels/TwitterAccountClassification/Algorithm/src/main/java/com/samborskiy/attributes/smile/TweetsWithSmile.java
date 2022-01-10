package com.samborskiy.attributes.smile;

import com.samborskiy.entity.Attribute;
import com.samborskiy.entity.sequences.SmileSequence;

import java.util.List;

/**
 * Frequency of tweet with smiles per account.
 *
 * @author Whiplash
 */
public class TweetsWithSmile extends SmileFunction {

    private final SmileSequence smile;

    public TweetsWithSmile(SmileSequence smile) {
        this.smile = smile;
    }

    @Override
    public String getName() {
        return String.format("tweets_with_%s", smile.toString());
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (String tweet : tweets) {
            count += smile.contains(tweet) ? 1 : 0;
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
