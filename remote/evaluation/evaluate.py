import os
import numpy as np
import pandas as pd
from ..readers import NumpyVideo


class Experiment:

    def __init__(self, validator, bpm, spo2):
        self.validator = validator
        self.bpm = bpm
        self.spo2 = spo2


def _build_dataset(base_df, experiments):
    df = base_df
    for i in range(len(experiments) - 1):
        df = pd.concat([df, base_df])
    df = df.sort_values(by='file').reset_index().drop('index', axis=1)
    cases = pd.DataFrame.from_dict({'validator': [e.validator for e in experiments],
                                    'bpm_estimator': [e.bpm for e in experiments],
                                    'spo2_estimator': [e.spo2 for e in experiments]})
    cases_df = cases
    for i in range(len(base_df) - 1):
        cases_df = pd.concat([cases_df, cases])
    cases_df = cases_df.reset_index().drop('index', axis=1)
    df = pd.concat([df, cases_df], axis=1)
    return df


def percentual_difference(y_true, y_pred):
    return np.abs(y_true - y_pred) / y_true


def evaluate(meta_path, data_dir, experiments):
    base_df = pd.read_csv(meta_path)
    df = _build_dataset(base_df, experiments)
    column_index = {col:(i+1) for i, col in enumerate(df.columns)}

    correctness = []
    bpms = []
    spo2s = []
    durations = []
    for row in df.itertuples():
        print(f"""Evaluating {row[column_index.get('file')]}, validating with {row[column_index.get('validator')]},
estimating BPM with {row[column_index.get('bpm_estimator')]} and SpO2 with {row[column_index.get('spo2_estimator')]}""")
        vid = NumpyVideo(os.path.join(data_dir, row[column_index.get('file')]))
        durations.append(len(vid.frames)/vid.fps)
        _, results = row[column_index.get('validator')].validate(vid)
        correctness.append(np.mean(results['result']))
        bpms.append(row[column_index.get('bpm_estimator')].measure(vid))
        spo2s.append(row[column_index.get('spo2_estimator')].measure(vid))
    df['duration'] = durations
    df['correctness'] = correctness
    df['predicted_bpm'] = bpms
    df['predicted_spo2'] = spo2s
    df['percentual_error_bpm'] = percentual_difference(df['bpm'], df['predicted_bpm'])
    df['percentual_error_spo2'] = percentual_difference(df['spo2'], df['predicted_spo2'])
    return df
    


