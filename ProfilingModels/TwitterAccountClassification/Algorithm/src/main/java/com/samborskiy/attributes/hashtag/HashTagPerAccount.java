package com.samborskiy.attributes.hashtag;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of use of hashtags per tweet.
 *
 * @author Whiplash
 */
public class HashTagPerAccount extends HashTagFunction {

    @Override
    public String getName() {
        return "hash_tag_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        attributes.add(new Attribute(tweets.stream()
                .mapToDouble(t -> getHashTags(t).size())
                .average().getAsDouble(), getName()));
    }
}
