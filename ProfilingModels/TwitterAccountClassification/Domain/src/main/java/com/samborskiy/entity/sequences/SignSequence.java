package com.samborskiy.entity.sequences;

/**
 * Sequence of signs.
 *
 * @author Whiplash
 */
public class SignSequence extends Sequence<String> {

    public SignSequence(String name, String... sequence) {
        super(name, sequence);
    }

    @Override
    public int count(String tweet) {
        int number = 0;
        for (String sign : sequence) {
            for (int i = 0; i < tweet.length(); i++) {
                int pos = 0;
                while ((pos = tweet.indexOf(sign, pos)) != -1) {
                    number++;
                    pos++;
                }
            }
        }
        return number;
    }
}
