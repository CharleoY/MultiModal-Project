package com.samborskiy.attributes.hashtag;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of use of references per tweet.
 *
 * @author Whiplash
 */
public class HashTagLength extends HashTagFunction {

    @Override
    public String getName() {
        return "hash_tag_length";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double length = 0.;
        for (String tweet : tweets) {
            for (String hashTag : getHashTags(tweet)) {
                length += hashTag.length();
            }
        }
        attributes.add(new Attribute(length / tweets.size(), getName()));
    }
}
