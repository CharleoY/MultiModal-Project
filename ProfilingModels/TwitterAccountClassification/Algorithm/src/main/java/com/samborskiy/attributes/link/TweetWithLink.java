package com.samborskiy.attributes.link;

import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Frequency of tweets with links per account.
 *
 * @author Whiplash
 */
public class TweetWithLink extends LinkAttributeFunction {

    @Override
    public String getName() {
        return "tweets_with_urls";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        float tweetsWithUrls = 0;
        for (String tweet : tweets) {
            tweetsWithUrls += urlsCount(tweet) > 0 ? 1 : 0;
        }
        attributes.add(new Attribute(tweetsWithUrls / tweets.size(), getName()));
    }
}
