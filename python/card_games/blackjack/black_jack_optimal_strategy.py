import pandas as pd

bj_optimal_df = pd.read_csv('black_jack_optimal_strategy.csv')

def get_action(score, score_dealer, hard, cards_paired):

    hard_or_soft_df = bj_optimal_df[bj_optimal_df['hard'] == hard]
    scores_df = hard_or_soft_df[hard_or_soft_df['score_dealer'] == score_dealer]
    score_df = hard_or_soft_df[scores_df['score'] == score]
    should_split = False
    if cards_paired:
        should_split = score_df['should_split']
    
    return {
        'decision': score_df['decision'],
        'should_split': should_split
    }