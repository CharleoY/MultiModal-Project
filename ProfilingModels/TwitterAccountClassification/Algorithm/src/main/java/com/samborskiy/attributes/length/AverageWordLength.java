package com.samborskiy.attributes.length;

import com.samborskiy.entity.Attribute;

import java.util.ArrayList;
import java.util.List;

/**
 * Frequency of words per account.
 *
 * @author Whiplash
 */
public class AverageWordLength extends LengthFunction {

    @Override
    public String getName() {
        return "average_word_length";
    }

    @Override
    protected List<Attribute> count(List<List<String>> tweets) {
        List<Attribute> attributes = new ArrayList<>();
        double lengthOfWords = 0.;
        int count = 0;
        for (List<String> tweet : tweets) {
            count += tweet.size();
            for (String word : tweet) {
                lengthOfWords += word.length();
            }
        }
        attributes.add(new Attribute(lengthOfWords / count, getName()));
        return attributes;
    }
}
