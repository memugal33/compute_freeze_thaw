# compute_freeze_thaw cycle 

This code classify the soil state for the WEPP output based on the daily frozen water value for the three different precipitation zone of the study.

Temperature data and water balance data is first used to compute the soil state (frozen vs thawing) using ```Main_analysis.py```

Then this classification is again used to compute the number of Freeze-Thaw cycle using ```Sub_ana_count_freeze_thaw_cycle.py```

```analyze_freeze_thaw_method_2.py``` and ```count_freeze_thaw_method2.py``` are two different set of function script use for the analysis.
