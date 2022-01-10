package com.samborskiy.attributes.reference;

import com.samborskiy.attributes.AttributeFunction;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Function based on using reference (mention) in account.
 *
 * @author Whiplash
 */
public abstract class ReferenceFunction extends AttributeFunction {

    protected List<String> getReferences(String tweet) {
        Pattern pattern = Pattern.compile("@(\\w)+");
        Matcher matcher = pattern.matcher(tweet);
        List<String> hashTags = new ArrayList<>();
        while (matcher.find()) {
            hashTags.add(matcher.group(0));
        }
        return hashTags;
    }
}
