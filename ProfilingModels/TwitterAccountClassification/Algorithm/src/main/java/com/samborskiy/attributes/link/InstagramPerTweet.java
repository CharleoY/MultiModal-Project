package com.samborskiy.attributes.link;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of instagram links per tweet.
 *
 * @author Whiplash
 */
public class InstagramPerTweet extends LinkAttributeFunction {

    @Override
    public String getName() {
        return "instagram_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        float urlsPerTweet = 0;
        for (String tweet : tweets) {
            urlsPerTweet += instagramCount(tweet);
        }
        attributes.add(new Attribute(urlsPerTweet / tweets.size(), getName()));
    }
}
