import pickle

with open('O_code.pkl', 'rb') as f:
    O_code = pickle.load(f)

values = list(O_code.values())
single_scores = {}
for value in values:
    for i in range(8):
        state = str(i) + value
        single_scores[state] = int(value[0]) + int(value[1]) * 3

combine_scores = {}
for s1 in single_scores:
    for s2 in single_scores:
        if int(s1[0]) != int(s2[0]):
            # caculate the factor
            i = int(s1[0])
            j = int(s2[0])
            # 45°
            if j - i == 1 or j - i == 7:
                factor = 1.5
            # 180°
            elif j - i == 4:
                factor = 2
            # 90°
            elif j - i == 2 or j - i == 6:
                factor = 1.2
            # 135°
            elif j - i == 3 or j - i == 5:
                factor = 1
            score = (single_scores[s1] + single_scores[s2]) * factor
            state = s1 + s2
            combine_scores[state] = round(score, 3)

pickle.dump(combine_scores, open('scores_board_6_1.pkl', 'wb'))

scores = {}
d = [str(i) for i in range(8)]


for v0 in values:
    state = v0
    for v1 in values:
        state += v1
        for v2 in values:
            state += v2
            for v3 in values:
                state += v3
                for v4 in values:
                    state += v4
                    for v5 in values:
                        state += v5
                        for v6 in values:
                            state += v6
                            for v7 in values:
                                state += v7

                                score = 0
                                for i in range(0, 16, 2):
                                    pre = str(int(i // 2))
                                    s1 = pre + state[i:i + 2]
                                    for j in range(i + 2, 16, 2):
                                        pre = str(int(j // 2))
                                        s2 = pre + state[j:j + 2]
                                        combine_state = s1 + s2
                                        score += combine_scores[combine_state]

                                scores[state] = score

pickle.dump(scores, open('scores_board_6_2.pkl', 'wb'))
