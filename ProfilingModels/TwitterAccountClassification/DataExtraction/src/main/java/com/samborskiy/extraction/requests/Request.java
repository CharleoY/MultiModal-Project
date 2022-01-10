package com.samborskiy.extraction.requests;

import com.samborskiy.entity.Log;
import com.samborskiy.extraction.utils.TwitterHelper;
import twitter4j.HttpResponseCode;
import twitter4j.TwitterException;

import java.util.Date;
import java.util.concurrent.TimeUnit;

/**
 * Abstract class to make a request to twitter API.
 *
 * @param <V> type of request result
 * @author Whiplash
 */
public abstract class Request<V> {

    /**
     * Time you want to wait to re-query API.
     */
    private static final long API_RESTART = TimeUnit.MINUTES.toMillis(15);

    private final TwitterHelper twitterHelper;

    /**
     * Creates instance of {@code Request}.
     *
     * @param twitterHelper {@link #twitterHelper}
     */
    public Request(TwitterHelper twitterHelper) {
        this.twitterHelper = twitterHelper;
    }

    /**
     * Returns helper to get access to twitter API.
     *
     * @return helper to get access to twitter API
     */
    protected TwitterHelper getTwitterHelper() {
        return twitterHelper;
    }

    /**
     * Returns result of request.
     *
     * @return result of request
     * @throws TwitterException if twitter service or network is unavailable
     */
    protected abstract V run() throws TwitterException;

    /**
     * Returns result of request (wrapper over method {@link #run()}).
     *
     * @return result of request
     * @throws InterruptedException if thread is interrupted
     */
    public V make() throws InterruptedException {
        try {
            return run();
        } catch (TwitterException e) {
            switch (e.getStatusCode()) {
                case HttpResponseCode.NOT_FOUND:
                    Log.e("Get user throw error: 404");
                    return null;
                case HttpResponseCode.TOO_MANY_REQUESTS:
                    Log.d("Exceeded the number of requests at " + new Date().toString());
                    Thread.sleep(API_RESTART);
                    return make();
            }
            return null;
        }
    }

}
