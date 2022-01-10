package com.samborskiy.attributes.sign;

import com.samborskiy.entity.sequences.SignSequence;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Latitude author use punctuation, equal to the maximum on the
 * number of different signs in sentences, divided by the number
 * of possible characters.
 */
public class SignLatitude extends SignFunction {

    @Override
    public String getName() {
        return "sign_latitude";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double max = 0;
        for (String tweet : tweets) {
            double count = 0.;
            for (SignSequence sequence : SIGNS) {
                count += sequence.contains(tweet) ? 1 : 0;
            }
            max = Math.max(max, count);
        }
        attributes.add(new Attribute(max / SIGNS.size(), getName()));
    }
}
