package com.samborskiy.attributes.vocabulary;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Attribute;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Number of different words used in tweets, divided by the total number of tweets the user.
 *
 * @author Whiplash
 */
public class RichnessOfVocabulary extends AttributeFunction {

    @Override
    public String getName() {
        return "richness_of_vocabulary";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        Set<String> words = new HashSet<>();
        for (String tweet : tweets) {
            words.addAll(tweetParser.parse(tweet));
        }
        attributes.add(new Attribute(((double) words.size()) / tweets.size(), getName()));
    }
}
