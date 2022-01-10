package com.samborskiy.attributes.hashtag;

import com.samborskiy.attributes.AttributeFunction;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Function based on the user's use of hashtags.
 *
 * @author Whiplash
 */
public abstract class HashTagFunction extends AttributeFunction {

    protected List<String> getHashTags(String tweet) {
        Pattern pattern = Pattern.compile("#(\\w)+");
        Matcher matcher = pattern.matcher(tweet);
        List<String> hashTags = new ArrayList<>();
        while (matcher.find()) {
            hashTags.add(matcher.group(0));
        }
        return hashTags;
    }
}
