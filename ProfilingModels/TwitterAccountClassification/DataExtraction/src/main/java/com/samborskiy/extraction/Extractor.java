package com.samborskiy.extraction;

import com.samborskiy.entity.Log;
import com.samborskiy.extraction.entity.Configuration;
import com.samborskiy.extraction.entity.Type;
import com.samborskiy.extraction.requests.TweetsRequest;
import com.samborskiy.extraction.requests.UserRequest;
import com.samborskiy.extraction.utils.DatabaseHelper;
import com.samborskiy.extraction.utils.TwitterHelper;
import twitter4j.User;

import java.io.File;
import java.util.List;

public class Extractor {

    private final File configurationFile;

    public Extractor(File configurationFile) {
        this.configurationFile = configurationFile;
    }

    public void update() throws Exception {
        Configuration configuration = Configuration.build(configurationFile);
        TwitterHelper twitterHelper = new TwitterHelper(configuration);

        try (DatabaseHelper dbHelper = new DatabaseHelper(configuration)) {
//            if (!new File(configuration.getDatabasePath()).exists()) {
//                dbHelper.createTable();
//            }
            for (Type type : configuration) {
                getUsers(type.getData().extractScreenNames(), twitterHelper, type, dbHelper);
                getUsers(type.getData().extractUserIds(), twitterHelper, type, dbHelper);
            }
            dbHelper.deleteEmptyTweetsRow();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private <E> void getUsers(List<E> identities, TwitterHelper twitterHelper, Type type, DatabaseHelper dbHelper) throws InterruptedException {
        User user = null;
        for (E identity : identities) {
            Log.d("Try get: " + identity.toString());
            if (identity instanceof String) {
                user = getUser((String) identity, twitterHelper, dbHelper);
            } else if (identity instanceof Long) {
                user = getUser((Long) identity, twitterHelper, dbHelper);
            }
            if (user != null) {
                tweetsExtraction(twitterHelper, dbHelper, type, user);
            }
        }
    }

    private User getUser(String screenName, TwitterHelper twitterHelper, DatabaseHelper dbHelper) throws InterruptedException {
        if (!dbHelper.hasUser(screenName)) {
            return new UserRequest(twitterHelper, screenName).make();
        }
        Log.d(String.format("Skip user %s", screenName));
        return null;
    }

    private User getUser(Long userId, TwitterHelper twitterHelper, DatabaseHelper dbHelper) throws InterruptedException {
        if (!dbHelper.hasUser(userId)) {
            return new UserRequest(twitterHelper, userId).make();
        }
        Log.d(String.format("Skip user %d", userId));
        return null;
    }

    private void tweetsExtraction(TwitterHelper twitterHelper, DatabaseHelper dbHelper, Type type, User user) throws InterruptedException {
        String tweets = new TweetsRequest(twitterHelper, user, type.getTweetPerUser()).make();
        dbHelper.insert(user.getId(), user, tweets, type.getId());
        Log.d(String.format("Get information about %s: %s", type.getName(), user.getScreenName()));
    }
}
