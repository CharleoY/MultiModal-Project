package com.samborskiy.attributes.link;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Account;
import com.samborskiy.entity.Attribute;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Function based on the links (urls).
 *
 * @author Whiplash
 */
public abstract class LinkAttributeFunction extends AttributeFunction {

    protected static final String URL_REGEX = "\\b(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]";
    protected static final String INSTAGRAM = "instag";

    @Override
    public List<Attribute> apply(Account account) {
        List<Attribute> attributes = new ArrayList<>();
        apply(attributes, account.getTweets());
        return attributes;
    }

    protected int urlsCount(String tweet) {
        int urlCount = 0;
        Pattern pattern = Pattern.compile(URL_REGEX);
        Matcher matcher = pattern.matcher(tweet);
        while (matcher.find()) {
            urlCount++;
        }
        return urlCount;
    }

    protected int instagramCount(String tweet) {
        int instagramCount = 0;
        int lastIndex = 0;
        while ((lastIndex = tweet.indexOf(INSTAGRAM, lastIndex + 1)) != -1) {
            instagramCount++;
            lastIndex += INSTAGRAM.length();
        }
        return instagramCount;
    }
}
