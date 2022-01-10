package com.samborskiy.entity.sequences;

import java.util.Arrays;
import java.util.List;

/**
 * Structure for holding sequence of elements with name.
 *
 * @param <E> type of holding elements
 */
public abstract class Sequence<E> {

    protected final String name;
    protected final List<E> sequence;

    public Sequence(String name, E... sequence) {
        this.name = name;
        this.sequence = Arrays.asList(sequence);
    }

    /**
     * Number of elements of sequence in tweet.
     *
     * @param tweet tweet that will be searched
     * @return number of elements of sequence in tweet
     */
    public abstract int count(String tweet);

    /**
     * Checks if elements of sequence contains in tweet.
     *
     * @param tweet tweet that will be searched
     * @return {@code true} if tweet contains elements of sequence, {@code false} otherwise
     */
    public boolean contains(String tweet) {
        return count(tweet) > 0;
    }

    @Override
    public String toString() {
        return name;
    }
}
