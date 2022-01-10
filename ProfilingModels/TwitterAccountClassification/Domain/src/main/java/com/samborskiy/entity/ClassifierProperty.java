package com.samborskiy.entity;

import com.samborskiy.entity.analyzers.frequency.FrequencyAnalyzer;
import com.samborskiy.entity.analyzers.grammar.GrammarAnalyzer;
import com.samborskiy.entity.analyzers.morphological.MorphologicalAnalyzer;
import com.samborskiy.entity.analyzers.sentence.TweetParser;
import org.reflections.Reflections;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Modifier;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;

public class ClassifierProperty {

    private static FrequencyAnalyzer frequencyAnalyzer = FrequencyAnalyzer.get();
    private static GrammarAnalyzer grammarAnalyzer = GrammarAnalyzer.get();
    private static MorphologicalAnalyzer morphologicalAnalyzer = MorphologicalAnalyzer.get();
    private static TweetParser tweetParser = TweetParser.get();
    private static Set<String> attributes;
    private static boolean isDebug = false;

    public static final String DEFAULT_FREQUENCY_ANALYZER = "com.samborskiy.entity.analyzers.frequency.FrequencyDictionary";
    public static final String DEFAULT_GRAMMAR_ANALYZER = "com.samborskiy.entity.analyzers.grammar.JLanguageToolGrammarCheckerRu";
    public static final String DEFAULT_MORPHOLOGICAL_ANALYZER = "com.samborskiy.entity.analyzers.morphological.SimpleMorphologicalAnalyzer";
    public static final String DEFAULT_SENTENCE_ANALYZER = "com.samborskiy.entity.analyzers.sentence.SimpleTweetParser";

    static {
        try (InputStream stream = new FileInputStream("twitter_classifier.properties")) {
            Properties properties = new Properties();
            properties.load(stream);
            frequencyAnalyzer = getClass(properties.getProperty("frequency_analyzer", DEFAULT_FREQUENCY_ANALYZER), FrequencyAnalyzer.class);
            grammarAnalyzer = getClass(properties.getProperty("grammar_analyzer", DEFAULT_GRAMMAR_ANALYZER), GrammarAnalyzer.class);
            morphologicalAnalyzer = getClass(properties.getProperty("morphological_analyzer", DEFAULT_MORPHOLOGICAL_ANALYZER), MorphologicalAnalyzer.class);
            tweetParser = getClass(properties.getProperty("sentence_analyzer", DEFAULT_SENTENCE_ANALYZER), TweetParser.class);
            attributes = getAttributes(properties.getProperty("random_forest_attributes", null));
            isDebug = Boolean.parseBoolean(properties.getProperty("debug", "false"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private ClassifierProperty() {
    }

    private static Set<String> getAttributes(String fileName) {
        if (fileName == null) {
            return null;
        }
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            Set<String> attributes = new HashSet<>();
            String attribute;
            while ((attribute = reader.readLine()) != null) {
                attributes.add(attribute);
            }
            return attributes;
        } catch (IOException e) {
            return null;
        }
    }

    private static <E> E getClass(String packageName, Class<E> type) throws ReflectiveOperationException {
        Reflections reflections = new Reflections(packageName);
        Set<Class<? extends E>> allClasses = reflections.getSubTypesOf(type);
        for (Class clazz : allClasses) {
            if (!Modifier.isAbstract(clazz.getModifiers())) {
                return (E) clazz.newInstance();
            }
        }
        return null;
    }

    public static FrequencyAnalyzer getFrequencyAnalyzer() {
        return frequencyAnalyzer;
    }

    public static GrammarAnalyzer getGrammarAnalyzer() {
        return grammarAnalyzer;
    }

    public static MorphologicalAnalyzer getMorphologicalAnalyzer() {
        return morphologicalAnalyzer;
    }

    public static TweetParser getTweetParser() {
        return tweetParser;
    }

    public static Set<String> getAttributes() {
        return attributes;
    }

    public static boolean isDebug() {
        return isDebug;
    }
}
