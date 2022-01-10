package com.samborskiy.attributes.smile;

import com.samborskiy.entity.Attribute;
import com.samborskiy.entity.sequences.SmileSequence;

import java.util.List;

/**
 * Frequency of use of any of smiles.
 *
 * @author Whiplash
 */
public class TweetsWithSmiles extends SmileFunction {

    @Override
    public String getName() {
        return "tweets_with_smiles";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (String tweet : tweets) {
            for (SmileSequence smile : SMILES) {
                if (smile.contains(tweet)) {
                    count++;
                    break;
                }
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
