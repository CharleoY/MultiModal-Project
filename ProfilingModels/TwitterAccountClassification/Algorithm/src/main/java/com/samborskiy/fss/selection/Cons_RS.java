package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.ConsistencySubsetEval;
import weka.attributeSelection.RankSearch;

/**
 * Consistency feature selection algorithm.
 *
 * @author Whiplash
 */
public class Cons_RS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new RankSearch();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new ConsistencySubsetEval();
    }
}
