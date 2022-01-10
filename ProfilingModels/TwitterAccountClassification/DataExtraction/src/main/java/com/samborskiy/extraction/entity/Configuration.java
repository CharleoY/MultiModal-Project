package com.samborskiy.extraction.entity;


import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.samborskiy.extraction.utils.EntityUtil;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Iterator;
import java.util.List;
import java.util.Spliterator;
import java.util.function.Consumer;

/**
 * Class stores the configuration for the selected language.
 *
 * @author Whiplash
 */
public class Configuration implements Iterable<Type> {

    private final Language lang;
    private final String databasePath;
    private final List<Type> types;

    @JsonCreator
    public Configuration(@JsonProperty("lang") Language lang,
                         @JsonProperty("databasePath") String databasePath,
                         @JsonProperty("types") List<Type> types) {
        this.lang = lang;
        this.databasePath = databasePath;
        this.types = types;
    }

    /**
     * Builds new instance of {@code Configuration} parsing {@code jsonData}.
     *
     * @param configFile configuration file (in json format)
     * @return {@code Configuration} constructed from json
     */
    public static Configuration build(File configFile) {
        try {
            byte[] jsonData = Files.readAllBytes(configFile.toPath());
            return EntityUtil.deserialize(jsonData, Configuration.class);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    @JsonProperty("lang")
    public Language getLang() {
        return lang;
    }

    @JsonProperty("databasePath")
    public String getDatabasePath() {
        return databasePath;
    }

    @JsonProperty("types")
    public List<Type> getTypes() {
        return types;
    }


    @Override
    public Iterator<Type> iterator() {
        return types.iterator();
    }

    @Override
    public void forEach(Consumer<? super Type> action) {
        types.forEach(action);
    }

    @Override
    public Spliterator<Type> spliterator() {
        return types.spliterator();
    }
}
