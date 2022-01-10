package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.Ranker;
import weka.attributeSelection.ReliefFAttributeEval;

/**
 * Distance feature selection algorithm.
 *
 * @author Whiplash
 */
public class Relief_F extends FeatureSelection {

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
        return new ReliefFAttributeEval();
    }
}
