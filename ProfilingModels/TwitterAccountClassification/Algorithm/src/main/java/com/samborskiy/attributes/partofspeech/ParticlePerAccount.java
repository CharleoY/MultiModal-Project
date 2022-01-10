package com.samborskiy.attributes.partofspeech;

import com.samborskiy.attributes.AttributeFunction;
import com.samborskiy.entity.Attribute;

import java.util.List;

/**
 * Number of appearance particle 'не' in the tweets divided by the total number of tweets.
 */
public class ParticlePerAccount extends AttributeFunction {

    private static final String NEGATIVE_PARTICLE = "не";

    @Override
    public String getName() {
        return "particle_ne_per_tweet";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0.;
        for (String tweet : tweets) {
            int index = 0;
            while ((index = tweet.indexOf(NEGATIVE_PARTICLE, index)) != -1) {
                count++;
                index++;
            }
        }
        attributes.add(new Attribute(count / tweets.size(), getName()));
    }
}
