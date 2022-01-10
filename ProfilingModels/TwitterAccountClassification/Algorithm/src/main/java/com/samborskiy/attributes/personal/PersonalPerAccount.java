package com.samborskiy.attributes.personal;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of personal words per account.
 *
 * @author Whiplash
 */
public class PersonalPerAccount extends PersonalFunction {

    @Override
    public String getName() {
        return "personal_words_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0.;
        for (String tweet : tweets) {
            count += match(tweet);
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
