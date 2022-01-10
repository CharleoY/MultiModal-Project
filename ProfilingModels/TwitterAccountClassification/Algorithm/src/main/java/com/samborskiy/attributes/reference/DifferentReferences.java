package com.samborskiy.attributes.reference;

import com.samborskiy.entity.Attribute;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Frequency of difference references per tweet.
 *
 * @author Whiplash
 */
public class DifferentReferences extends ReferenceFunction {

    @Override
    public String getName() {
        return "different_references_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        Set<String> references = new HashSet<>();
        for (String tweet : tweets) {
            references.addAll(getReferences(tweet.toLowerCase()).stream().collect(Collectors.toList()));
        }
        attributes.add(new Attribute(((double) references.size()) / tweets.size(), getName()));
    }
}
