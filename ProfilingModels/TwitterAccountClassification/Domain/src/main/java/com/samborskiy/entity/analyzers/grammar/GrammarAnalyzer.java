package com.samborskiy.entity.analyzers.grammar;

import java.io.IOException;

/**
 * Analyzer of grammar.
 *
 * @author Whiplash
 */
public abstract class GrammarAnalyzer {

    private static final GrammarAnalyzer analyzer = new JLanguageToolGrammarCheckerRu();

    public static GrammarAnalyzer get() {
        return analyzer;
    }

    /**
     * Checks grammar error of text.
     *
     * @param text text to be examined for errors
     * @return number of errors
     */
    public abstract int check(String text) throws IOException;
}
