package com.samborskiy.extraction.requests;

import com.samborskiy.extraction.utils.TwitterHelper;
import twitter4j.TwitterException;
import twitter4j.User;

/**
 * Request to get user's tweets.
 *
 * @author Whiplash
 */
public class TweetsRequest extends Request<String> {

    private final User user;
    private final int number;

    /**
     * Creates instance of {@code FindUsersRequest}.
     *
     * @param twitterHelper to get access to twitter API
     * @param user          user who will take tweets
     * @param number        number of required tweets
     */
    public TweetsRequest(TwitterHelper twitterHelper, User user, int number) {
        super(twitterHelper);
        this.user = user;
        this.number = number;
    }

    @Override
    protected String run() throws TwitterException {
        return getTwitterHelper().getTweets(user.getScreenName(), number);
    }

}
