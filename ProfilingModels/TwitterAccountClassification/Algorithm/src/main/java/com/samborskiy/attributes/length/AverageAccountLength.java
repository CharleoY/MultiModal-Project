package com.samborskiy.attributes.length;

import com.samborskiy.entity.Attribute;

import java.util.ArrayList;
import java.util.List;

/**
 * Frequency of tweets per account.
 *
 * @author Whiplash
 */
public class AverageAccountLength extends LengthFunction {

    @Override
    public String getName() {
        return "average_tweet_length";
    }

    @Override
    protected List<Attribute> count(List<List<String>> tweets) {
        List<Attribute> attributes = new ArrayList<>();
        attributes.add(new Attribute(tweets.stream()
                .mapToDouble(List::size)
                .average().getAsDouble(), getName()));
        return attributes;
    }
}
