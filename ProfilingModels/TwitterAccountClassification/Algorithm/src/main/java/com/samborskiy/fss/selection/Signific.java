package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.Ranker;
import weka.attributeSelection.SignificanceAttributeEval;

/**
 * Probabilistic significance feature selection algorithm.
 *
 * @author Whiplash
 */
public class Signific extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new Ranker();
    }

    @Override
    protected String[] getSearcherOptions() {
        return new String[]{"-T", "0.01"};
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new SignificanceAttributeEval();
    }
}
