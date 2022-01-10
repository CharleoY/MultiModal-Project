package com.samborskiy.attributes.sign;

import com.samborskiy.entity.sequences.SignSequence;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of different signs in a tweets.
 */
public class AvrSignsNumber extends SignFunction {

    @Override
    public String getName() {
        return "average_signs_number";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0.;
        for (String tweet : tweets) {
            for (SignSequence sequence : SIGNS) {
                count += sequence.contains(tweet) ? 1 : 0;
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
