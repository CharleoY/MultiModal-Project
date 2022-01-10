package com.samborskiy.attributes.reference;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * References length divided by the number of tweets.
 *
 * @author Whiplash
 */
public class ReferenceLength extends ReferenceFunction {

    @Override
    public String getName() {
        return "reference_length";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double length = 0.;
        for (String tweet : tweets) {
            for (String reference : getReferences(tweet)) {
                length += reference.length();
            }
        }
        attributes.add(new Attribute(length / tweets.size(), getName()));
    }
}
