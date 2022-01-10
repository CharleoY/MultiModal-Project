package com.samborskiy.extraction.entity;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Class to keep configure information where and how get data for sample.
 *
 * @author Whiplash
 */
public class Data {

    private final String userIds;
    private final String screenNames;

    @JsonCreator
    public Data(@JsonProperty("userIds") String userIds,
                @JsonProperty("screenNames") String screenNames) {
        this.userIds = userIds;
        this.screenNames = screenNames;
    }

    @JsonProperty("userIds")
    public String getUserIds() {
        return userIds;
    }

    @JsonProperty("screenNames")
    public String getScreenNames() {
        return screenNames;
    }

    public List<Long> extractUserIds() {
        return getData(userIds).stream().map(Long::parseLong).collect(Collectors.toList());
    }

    public List<String> extractScreenNames() {
        return getData(screenNames);
    }

    private static List<String> getData(String fileName) {
        List<String> list = new ArrayList<>();
        try (BufferedReader bf = new BufferedReader(new FileReader(fileName))) {
            String str;
            while ((str = bf.readLine()) != null) {
                list.add(str);
            }
            bf.close();
        } catch (Exception ignored) {
        }
        return list;
    }

}
