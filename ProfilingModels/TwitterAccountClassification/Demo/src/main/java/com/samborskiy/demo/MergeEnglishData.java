package com.samborskiy.demo;

import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.User;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Set;
import java.util.stream.Collectors;

public class MergeEnglishData {

    public static void main(String[] args) throws IOException {
        try (BufferedReader reader1 = new BufferedReader(new FileReader("../res/en/corporate"));
             BufferedReader reader2 = new BufferedReader(new FileReader("../res/en/screen_names_1"))) {
            Set<Long> ids = reader1.lines().map(Long::parseLong).collect(Collectors.toSet());

            Twitter twitter = new TwitterFactory().getInstance();
            reader2.lines().forEach(screenName -> {
                try {
                    User user = twitter.showUser(screenName);
                    System.out.println(user.getId());
                    ids.add(user.getId());
                } catch (TwitterException e) {
                    e.printStackTrace();
                }
            });

            try (PrintWriter writer = new PrintWriter("en_corporate")) {
                ids.stream().forEach(writer::println);
            }
        }
    }
}
