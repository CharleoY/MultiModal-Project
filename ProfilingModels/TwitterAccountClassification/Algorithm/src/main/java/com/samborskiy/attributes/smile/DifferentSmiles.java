package com.samborskiy.attributes.smile;

import com.samborskiy.entity.Attribute;
import com.samborskiy.entity.sequences.SmileSequence;

import java.util.List;

/**
 * Number of different types of smiles encountered in tweets, divided by the number of types of smiles.
 *
 * @author Whiplash
 */
public class DifferentSmiles extends SmileFunction {

    @Override
    public String getName() {
        return "different_smiles";
    }

    @Override
    protected void apply(List<Attribute> attributes, List<String> tweets) {
        double count = 0;
        for (SmileSequence smile : SMILES) {
            for (String tweet : tweets) {
                if (smile.contains(tweet)) {
                    count++;
                    break;
                }
            }
        }
        attributes.add(new Attribute(count / SMILES.size(), getName()));
    }
}
