package com.samborskiy.attributes.hashtag;

import com.samborskiy.entity.Attribute;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Frequency of use of different hashtags per tweet.
 *
 * @author Whiplash
 */
public class DifferentHashTags extends HashTagFunction {

    @Override
    public String getName() {
        return "different_hash_tags_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        Set<String> hashTags = new HashSet<>();
        for (String tweet : tweets) {
            hashTags.addAll(getHashTags(tweet.toLowerCase()).stream().collect(Collectors.toList()));
        }
        attributes.add(new Attribute(((double) hashTags.size()) / tweets.size(), getName()));
    }
}
