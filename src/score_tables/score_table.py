import pickle
with open ('O_code.pkl', 'rb') as f:
    O_code = pickle.load(f)
O_code

values = list(O_code.values())
single_scores = {}
for value in values:
    for i in range(8):
        state = str(i) + value
        single_scores[state] = int(value[0]) + int(value[1]) * 3
single_scores

combine_scores = {}
for s1 in single_scores:
    for s2 in single_scores:
        if int(s1[0]) != int(s2[0]):
            # caculate the factor
            i = int(s1[0])
            j = int(s2[0])
            # 45°
            if j - i == 1 or j-i == 7:
                factor = 1.5
            # 180°
            elif j-i == 4:
                factor = 2
            # 90°
            elif j-i == 2 or j-i == 6 :
                factor = 1.2
            # 135°   
            elif j-i ==3 or j-i == 5:
                factor = 1
            score = (single_scores[s1] + single_scores[s2]) * factor
            state = s1+s2
            combine_scores[state] = round(score, 3)

pickle.dump(combine_scores,open('scores_board_6_1.pkl', 'wb'))

scores = {}
d = [str(i) for i in range(8)]
d


pickle.dump(scores,open('scores_board_6_2.pkl', 'wb'))
    