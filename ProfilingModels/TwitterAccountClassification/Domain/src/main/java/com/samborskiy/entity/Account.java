package com.samborskiy.entity;

import weka.core.DenseInstance;
import weka.core.Instance;

import java.util.ArrayList;
import java.util.List;

/**
 * Structure for handling information about Twitter account.
 */
public class Account extends ArrayList<Attribute> {

    protected final int classId;
    protected final List<String> tweets = new ArrayList<>();

    protected int followers;
    protected int following;
    protected int verified;
    protected int favourite;

    public Account(int classId, int followers, int following, int verified, int favourite) {
        super();
        this.classId = classId;
        this.followers = followers;
        this.following = following;
        this.verified = verified;
        this.favourite = favourite;
    }

    public void addTweet(String tweet) {
        tweets.add(tweet);
    }

    public void addTweets(List<String> tweets) {
        tweets.forEach(this::addTweet);
    }

    public List<String> getTweets() {
        return tweets;
    }

    public int getClassId() {
        return classId;
    }

    public int getFollowers() {
        return followers;
    }

    public int getFollowing() {
        return following;
    }

    public int getVerified() {
        return verified;
    }

    public int getFavourite() {
        return favourite;
    }

    /**
     * Converts account structure to instance.
     *
     * @param attrs list of attributes to add them into instance
     * @return built instance
     */
    public Instance toInstance(List<weka.core.Attribute> attrs) {
        Instance instance = new DenseInstance(attrs.size());
        Attribute classAttr = new Attribute(classId, "class");
        add(classAttr);
        for (Attribute attribute : this) {
            attrs.stream()
                    .filter(attr -> attribute.getName().equals(attr.name()))
                    .forEach(attr -> instance.setValue(attr, attribute.getValue()));
        }
        remove(classAttr);
        return instance;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Account account = (Account) o;
        return tweets.equals(account.tweets);
    }

    @Override
    public int hashCode() {
        return tweets != null ? tweets.hashCode() : 0;
    }
}
