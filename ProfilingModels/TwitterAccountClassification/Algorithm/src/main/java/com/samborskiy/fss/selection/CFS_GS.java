package com.samborskiy.fss.selection;

import com.samborskiy.fss.FeatureSelection;
import weka.attributeSelection.ASEvaluation;
import weka.attributeSelection.ASSearch;
import weka.attributeSelection.CfsSubsetEval;
import weka.attributeSelection.GeneticSearch;

/**
 * Dependency feature selection algorithm.
 *
 * @author Whiplash
 */
public class CFS_GS extends FeatureSelection {

    @Override
    protected ASSearch getSearcher() {
        return new GeneticSearch();
    }

    @Override
    protected ASEvaluation getEvaluator() {
        return new CfsSubsetEval();
    }
}
