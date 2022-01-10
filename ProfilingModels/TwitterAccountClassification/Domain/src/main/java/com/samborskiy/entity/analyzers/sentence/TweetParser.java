package com.samborskiy.entity.analyzers.sentence;

import java.util.List;

/**
 * Analyzer to parse tweet by word.
 *
 * @author Whiplash
 */
public abstract class TweetParser {

    private static final TweetParser parser = new SimpleTweetParser();

    /**
     * Returns words of tweet.
     *
     * @param tweet tweet which will be parsed
     * @return words of tweet
     */
    public abstract List<String> parse(String tweet);

    public static TweetParser get() {
        return parser;
    }
}
