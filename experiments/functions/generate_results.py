import pandas as pd
from sklearn import metrics

def results_summary(df_result_summary,fs_index,feature_sets_names,test_labels,y_pred):

    df_result_summary.at[fs_index, 'classifier'] = feature_sets_names[
        fs_index]
    df_result_summary.at[fs_index, 'TN'] = \
        metrics.confusion_matrix(test_labels, y_pred)[0][0]
    df_result_summary.at[fs_index, 'FP'] = \
        metrics.confusion_matrix(test_labels, y_pred)[0][1]
    df_result_summary.at[fs_index, 'FN'] = \
        metrics.confusion_matrix(test_labels, y_pred)[1][0]
    df_result_summary.at[fs_index, 'TP'] = \
        metrics.confusion_matrix(test_labels, y_pred)[1][1]
    df_result_summary.at[fs_index, 'F1'] = round(
        metrics.f1_score(test_labels,
                         y_pred,
                         average='weighted') * 100, 2)
    df_result_summary.at[fs_index, 'F1_macro'] = round(
        metrics.f1_score(test_labels,
                         y_pred,
                         average='macro') * 100, 2)
    df_result_summary.at[fs_index, 'Pr_macro'] = round(
        metrics.precision_score(
            test_labels, y_pred, average='macro') * 100, 2)
    df_result_summary.at[fs_index, 'R_macro'] = round(
        metrics.recall_score(test_labels,
                             y_pred,
                             average='macro') * 100, 2)
    df_result_summary.at[fs_index, 'Acc'] = round(
        metrics.accuracy_score(test_labels,
                               y_pred) * 100, 2)