package com.samborskiy.extraction;

import com.samborskiy.entity.Account;
import com.samborskiy.extraction.entity.Configuration;
import com.samborskiy.extraction.utils.DatabaseHelper;
import com.samborskiy.extraction.utils.EntityUtil;

import java.io.File;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Util to convert data stored in database to {@link com.samborskiy.entity.Account} structure.
 *
 * @author Whiplash
 */
public class DataToAccounts {

    private final File configurationFile;

    public DataToAccounts(File configurationFile) {
        this.configurationFile = configurationFile;
    }

    /**
     * Returns list of user {@link com.samborskiy.entity.Account} get from database.
     *
     * @return list of user {@link com.samborskiy.entity.Account} get from database
     */
    public List<Account> get() {
        Configuration configuration = Configuration.build(configurationFile);
        List<Account> instances = new ArrayList<>();
        try (DatabaseHelper databaseHelper = new DatabaseHelper(configuration)) {
            ResultSet cursor = databaseHelper.getAll();
            while (cursor.next()) {
                instances.add(cursorToAccount(cursor));
            }
            cursor.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return instances;
    }

    /**
     * Converts cursor to account structure.
     *
     * @param cursor pointer to database row
     * @return generate account structure
     * @throws SQLException if cursor is invalid
     * @throws IOException  incorrect tweets json
     */
    private Account cursorToAccount(ResultSet cursor) throws SQLException, IOException {
        Account account = new Account(cursor.getInt(DatabaseHelper.ACCOUNT_TYPE),
                cursor.getInt(DatabaseHelper.FOLLOWERS),
                cursor.getInt(DatabaseHelper.FOLLOWING),
                cursor.getInt(DatabaseHelper.VERIFIED),
                cursor.getInt(DatabaseHelper.VERIFIED));
        account.addTweets(parseRow(cursor));
        return account;
    }

    /**
     * Returns list of parsed tweets.
     *
     * @param cursor cursor on table row
     * @return list of parsed tweets
     * @throws java.sql.SQLException trouble with database connect
     * @throws java.io.IOException   incorrect tweets json
     */
    private List<String> parseRow(ResultSet cursor) throws SQLException, IOException {
        String[] tweets = EntityUtil.deserialize(cursor.getString(DatabaseHelper.TWEETS).getBytes(), String[].class);
        return Arrays.asList(tweets);
    }
}
