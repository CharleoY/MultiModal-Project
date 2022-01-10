package com.samborskiy.attributes;

import com.samborskiy.entity.Account;
import com.samborskiy.entity.Attribute;
import com.samborskiy.entity.ClassifierProperty;
import com.samborskiy.entity.analyzers.frequency.FrequencyAnalyzer;
import com.samborskiy.entity.analyzers.grammar.GrammarAnalyzer;
import com.samborskiy.entity.analyzers.morphological.MorphologicalAnalyzer;
import com.samborskiy.entity.analyzers.sentence.TweetParser;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

/**
 * Function to get attributes by account.
 *
 * @author Whiplash
 */
public abstract class AttributeFunction implements Function<Account, List<Attribute>> {

    private static final String URL_REGEX = "\\b(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]";

    protected static FrequencyAnalyzer frequencyAnalyzer = ClassifierProperty.getFrequencyAnalyzer();
    protected static GrammarAnalyzer grammarAnalyzer = ClassifierProperty.getGrammarAnalyzer();
    protected static MorphologicalAnalyzer morphologicalAnalyzer = ClassifierProperty.getMorphologicalAnalyzer();
    protected static TweetParser tweetParser = ClassifierProperty.getTweetParser();

    public abstract String getName();

    @Override
    public List<Attribute> apply(Account account) {
        List<String> tweets = account.getTweets();
        for (int i = 0; i < tweets.size(); i++) {
            tweets.set(i, tweets.get(i).replaceAll(URL_REGEX, " "));
        }
        List<Attribute> attributes = new ArrayList<>();
        apply(attributes, tweets);
        return attributes;
    }

    protected abstract void apply(List<Attribute> attributes, List<String> tweets);
}
