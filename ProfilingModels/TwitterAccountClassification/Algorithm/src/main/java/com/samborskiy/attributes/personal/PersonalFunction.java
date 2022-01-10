package com.samborskiy.attributes.personal;

import com.samborskiy.attributes.AttributeFunction;

import java.util.Arrays;

/**
 * Function based on personal words.
 *
 * @author Whiplash
 */
public abstract class PersonalFunction extends AttributeFunction {

    protected final String[] WORDS = {"я", "ты", "буду", "мой", "мне"};
    protected final String[] SUFFIXES = {"ил", "ыл", "ал", "ила", "ыла", "ала"};

    protected double match(String tweet) {
        double count = 0.;
        for (String word : tweetParser.parse(tweet)) {
            if (Arrays.asList(WORDS).contains(word)) {
                count++;
                continue;
            }
            for (String suffix : SUFFIXES) {
                if (word.endsWith(suffix)) {
                    count++;
                    break;
                }
            }
        }
        return count;
    }
}
