package com.samborskiy.extraction.utils;

import com.samborskiy.extraction.entity.Configuration;
import com.samborskiy.extraction.entity.Language;
import twitter4j.*;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Class which help user interact with twitter API.
 *
 * @author Whiplash
 */
public class TwitterHelper {

    private Configuration configuration;
    private Twitter twitter;

    /**
     * Creates new instance of {@code TwitterHelper} with
     * initialize {@code configuration}.
     *
     * @param configuration needed to connect to database and get
     *                      some parameters to data extraction
     */
    public TwitterHelper(Configuration configuration) {
        this.configuration = configuration;
        twitter = new TwitterFactory().getInstance();
    }

    /**
     * Returns information about user by screen name.
     *
     * @param userId id of user
     * @return information about user
     * @throws twitter4j.TwitterException if twitter service or network is unavailable
     */
    public User getUser(long userId) throws TwitterException {
        User user = twitter.showUser(userId);
        if (isCorrectUser(user)) {
            return user;
        }
        return null;
    }

    /**
     * Returns information about user by screen name.
     *
     * @param screenName screen name of user
     * @return information about user
     * @throws twitter4j.TwitterException if twitter service or network is unavailable
     */
    public User getUser(String screenName) throws TwitterException {
        User user = twitter.showUser(screenName);
        if (isCorrectUser(user)) {
            return user;
        }
        return null;
    }

    /**
     * Returns user tweets in json format.
     *
     * @param screenName  screen name of user
     * @param tweetNumber number of tweet per user
     * @return user tweets
     * @throws TwitterException if twitter service or network is unavailable
     */
    public String getTweets(String screenName, int tweetNumber) throws TwitterException {
        Paging paging = new Paging(1, tweetNumber);
        List<Status> statuses = twitter.getUserTimeline(screenName, paging);
        return EntityUtil.serialize(filterTweets(statuses));
    }

    /**
     * Returns filtered tweets of user.
     *
     * @param statuses user statuses (tweets)
     * @return user tweets
     */
    private List<String> filterTweets(List<Status> statuses) {
        List<String> tweets = new ArrayList<>();
        for (Status status : statuses) {
            if (!status.isRetweet() && configuration.getLang().equals(Language.fromString(status.getLang()))) {
                tweets.add(status.getText());
            }
        }
        return tweets;
    }

    /**
     * Returns list of users which was found by name.
     *
     * @param name name of user
     * @return list of users
     * @throws TwitterException if twitter service or network is unavailable
     */
    public List<User> findUsersByName(String name) throws TwitterException {
        Set<User> filteredUser = new HashSet<>();
        for (int page = 0; page < 5; page++) {
            filteredUser.addAll(getUsersPageByName(name, page));
        }
        return new ArrayList<>(filteredUser);
    }

    /**
     * Returns list of users from {@code page} by name.
     *
     * @param name name of user
     * @param page number of page
     * @throws TwitterException if twitter service or network is unavailable
     */
    private List<User> getUsersPageByName(String name, int page) throws TwitterException {
        List<User> filteredUser = new ArrayList<>();
        try {
            ResponseList<User> users = twitter.searchUsers(getQuery(name), page);
            filteredUser.addAll(users.stream().filter(this::isCorrectUser).collect(Collectors.toList()));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return filteredUser;
    }

    /**
     * Returns encoded query to {@code UTF-8}.
     *
     * @param name name of user
     * @return resulting query
     * @throws java.io.UnsupportedEncodingException if the named encoding is not supported
     */
    private String getQuery(String name) throws UnsupportedEncodingException {
        return "q=" + URLEncoder.encode(name, "UTF-8");
    }

    /**
     * Checks is correct user or not.
     *
     * @param user user whom will be checked
     * @return {@code true} if user is correct
     */
    private boolean isCorrectUser(User user) {
        return configuration.getLang().equals(Language.fromString(user.getLang()))
                && !user.isProtected() && user.getStatus() != null;
    }
}
