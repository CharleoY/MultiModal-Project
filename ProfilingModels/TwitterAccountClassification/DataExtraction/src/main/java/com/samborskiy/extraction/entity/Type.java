package com.samborskiy.extraction.entity;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Class to keep configure information about type.
 *
 * @author Whiplash
 */
public class Type {

    private final int id;
    private final int tweetPerUser;
    private final Data data;
    private final String name;

    @JsonCreator
    public Type(@JsonProperty("id") int id,
                @JsonProperty("tweetPerUser") int tweetPerUser,
                @JsonProperty("data") Data data,
                @JsonProperty("name") String name) {
        this.id = id;
        this.tweetPerUser = tweetPerUser;
        this.data = data;
        this.name = name;
    }

    @JsonProperty("id")
    public int getId() {
        return id;
    }

    @JsonProperty("tweetPerUser")
    public int getTweetPerUser() {
        return tweetPerUser;
    }

    @JsonProperty("data")
    public Data getData() {
        return data;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }
}
