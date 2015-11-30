from nw import NeedlemanWunsch
from itertools import combinations
from multiprocessing import Pool
import argparse


def align_similar(s1, s2):
    change1, change2 = list(), list()
    i = 0
    while s1 != s2:
        if i > len(s1) - 1:
            s1 += s2[i:]
            change1.extend(range(i, i + len(s2[i:])))
            continue
        if i > len(s2) - 1:
            s2 += s1[i:]
            change2.extend(range(i, i + len(s1[i:])))
            continue
        if s1[i] != s2[i]:
            if s1[i] == '-':
                s2 = s2[0:i] + '-' + s2[i:]
                change2.append(i)
            else:
                s1 = s1[0:i] + '-' + s1[i:]
                change1.append(i)
        i += 1
    return sorted(change1), sorted(change2)


def adjust(string_list, indices):
    for i, string in enumerate(string_list):
        for index in indices:
            string = string[:index] + '-' + string[index:]
        string_list[i] = string


def worker(it):
    ((i, string_i), (j, string_j)), scores = it
    model = NeedlemanWunsch(string_i, string_j, scores).nw(True)
    (string_ai, string_aj), score = model['nw'][0], model['score']
    return (i, string_ai), (j, string_aj), score


class CenterStar:

    def __init__(self, scores, strings):
        self.scores = scores
        self.strings = strings
        self.dp = [[0] * (len(strings) + 1) for _ in range(len(strings))]

    def msa(self):
        msa_result = []
        max_row, max_value = 0, 0
        len_strings = len(self.strings)

        tasks = tuple(combinations(zip(range(len_strings), self.strings), 2))
        tasks = zip(tasks, (self.scores for _ in range(len(tasks))))

        with Pool() as pool:
            result = pool.map(worker, tasks)
            for elem in result:
                (i, string_i), (j, string_j), score = elem
                ''' (0, 1, 2) => 0 is the first aligned string
                                 1 is the second aligned string
                                 2 is the score
                '''
                self.dp[i][j] = (string_i, string_j, score)
                self.dp[j][i] = (string_j, string_i, score)
                self.dp[i][-1] += score
                self.dp[j][-1] += score

                if self.dp[j][-1] > max_value:
                    max_row = j
                    max_value = self.dp[j][-1]
                if self.dp[i][-1] > max_value:
                    max_row = i
                    max_value = self.dp[i][-1]

            for i in range(len_strings):
                if i == max_row:
                    continue
                if not msa_result:
                    msa_result.extend(self.dp[max_row][i][0: 2])
                    continue

                new = list(self.dp[max_row][i][0: 2])
                ch_index1, ch_index2 = align_similar(msa_result[0], new[0])

                adjust(msa_result, ch_index1)
                adjust(new, ch_index2)
                msa_result.extend(new[1:])

        return msa_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Multiple sequence alignment')
    parser.add_argument("inputfile", help="input file location")
    parser.add_argument("outputfile", help="output file location")
    args = parser.parse_args()

    with open(args.inputfile, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        scores = lines.pop(0).split(',')
        msa = CenterStar(scores, lines).msa()

        with open(args.outputfile, 'w') as out:
            out.writelines(map(lambda x: x + '\n', msa))
