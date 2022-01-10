package com.samborskiy.entity.sequences;

/**
 * Sequence of smiles.
 *
 * @author Whiplash
 */
public class SmileSequence extends Sequence<String> {

    public SmileSequence(String name, String... sequence) {
        super(name, sequence);
    }

    @Override
    public int count(String tweet) {
        int number = 0;
        for (String smile : sequence) {
            for (int i = 0; i < tweet.length(); i++) {
                int pos = 0;
                while ((pos = tweet.indexOf(smile, pos)) != -1) {
                    number++;
                    pos++;
                }
            }
        }
        return number;
    }
}
