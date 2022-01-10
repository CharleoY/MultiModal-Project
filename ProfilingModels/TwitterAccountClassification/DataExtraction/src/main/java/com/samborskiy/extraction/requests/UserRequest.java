package com.samborskiy.extraction.requests;

import com.samborskiy.extraction.utils.TwitterHelper;
import twitter4j.TwitterException;
import twitter4j.User;

/**
 * Request to get information about user.
 *
 * @author Whiplash
 */
public class UserRequest extends Request<User> {

    private final String screenName;
    private final long userId;

    /**
     * Creates instance of {@code FindUsersRequest}.
     *
     * @param twitterHelper to get access to twitter API
     * @param screenName    screen name of user
     */
    public UserRequest(TwitterHelper twitterHelper, String screenName) {
        super(twitterHelper);
        this.screenName = screenName;
        this.userId = -1;
    }

    /**
     * Creates instance of {@code FindUsersRequest}.
     *
     * @param twitterHelper to get access to twitter API
     * @param userId        id of user
     */
    public UserRequest(TwitterHelper twitterHelper, long userId) {
        super(twitterHelper);
        this.screenName = null;
        this.userId = userId;
    }

    @Override
    protected User run() throws TwitterException {
        if (screenName == null) {
            return getTwitterHelper().getUser(userId);
        } else {
            return getTwitterHelper().getUser(screenName);
        }
    }

}
