package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.CfsSubsetEval;
import weka.attributeSelection.TabuSearch;

/**
 * Dependency feature selection algorithm.
 *
 * @author Whiplash
 */
public class CFS_TS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new TabuSearch();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new CfsSubsetEval();
    }
}
