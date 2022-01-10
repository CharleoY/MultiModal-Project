package com.samborskiy.attributes.grammar;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of errors (grammar, punctuation).
 *
 * @author Whiplash
 */
public class ErrorsPerAccount extends AttributeFunction {

    @Override
    public String getName() {
        return "errors_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0.;
        for (String tweet : tweets) {
            try {
                count += grammarAnalyzer.check(tweet);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
