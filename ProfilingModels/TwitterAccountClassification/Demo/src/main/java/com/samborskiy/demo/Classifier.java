package com.samborskiy.demo;

import com.samborskiy.TwitterAccountClassifier;
import com.samborskiy.entity.Account;
import com.samborskiy.extraction.DataToAccounts;

import java.io.File;
import java.util.List;

public class Classifier {

    public static void main(String[] args) throws Exception {
        DataToAccounts dataToAccounts = new DataToAccounts(new File("res/ru/config.json"));
        List<Account> accounts = dataToAccounts.get();

        TwitterAccountClassifier twitterAccountClassifier = new TwitterAccountClassifier("train");
        twitterAccountClassifier.build();
        int incorrect = 0;
        for (Account account : accounts) {
            if (twitterAccountClassifier.getClassId(account) != account.getClassId()) {
                incorrect++;
            }
        }
        System.out.println(incorrect);
    }
}
