package com.samborskiy.fss;

import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;

/**
 * Feature selection algorithm that does nothing
 * (need for test and find the best of feature selection algorithms).
 *
 * @author Whiplash
 */
public class NoFeatureSelection extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return null;
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return null;
    }
}
