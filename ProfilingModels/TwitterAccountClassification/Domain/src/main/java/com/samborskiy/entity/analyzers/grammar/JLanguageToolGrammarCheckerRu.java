package com.samborskiy.entity.analyzers.grammar;

import org.languagetool.JLanguageTool;
import org.languagetool.language.Russian;

import java.io.IOException;

/**
 * Grammar analyzer based on LanguageTool.
 *
 * @author Whiplash
 * @see <a href="https://languagetool.org/">LanguageTool</a>
 */
public class JLanguageToolGrammarCheckerRu extends GrammarAnalyzer {

    protected final JLanguageTool languageTool;

    public JLanguageToolGrammarCheckerRu() {
        this.languageTool = new JLanguageTool(new Russian());
    }

    @Override
    public int check(String text) throws IOException {
        return languageTool.check(text).size();
    }
}
