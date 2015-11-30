class NWCell:

    def __init__(self, score):
        self.score = score
        self.tracebacks = []


def get_initial_cells(n, m):
    return [[NWCell(0) for _ in range(n)] for _ in range(m)]


class NeedlemanWunsch:
    WEST = 'w'
    NORTH = 'n'
    NORTHWEST = 'nw'

    def __init__(self, string1, string2, scores):
        self.string1 = string1
        self.string2 = string2
        self.match, self.mismatch, self.gap = list(map(int, scores))
        self.dp = get_initial_cells(len(string2) + 1, len(string1) + 1)

    def nw(self, onlyOne=False):
        self.__prepare_matrix()

        for i in range(1, len(self.string1) + 1):
            for j in range(1, len(self.string2) + 1):
                north = self.dp[i - 1][j].score + self.gap
                west = self.dp[i][j - 1].score + self.gap
                northwest = self.dp[i - 1][j - 1].score

                if self.string1[i - 1] == self.string2[j - 1]:
                    northwest += self.match
                else:
                    northwest += self.mismatch

                max_ = max(northwest, west, north)
                self.dp[i][j].score = max_

                if max_ == north:
                    self.dp[i][j].tracebacks.append(NeedlemanWunsch.NORTH)
                if max_ == west:
                    self.dp[i][j].tracebacks.append(NeedlemanWunsch.WEST)
                if max_ == northwest:
                    self.dp[i][j].tracebacks.append(NeedlemanWunsch.NORTHWEST)

        return {'nw': self.__tracebacks(onlyOne),
                'score': self.dp[-1][-1].score}

    def __tracebacks(self, onlyOne):
        # (i,j,storedString1,StoredString2)
        stack = [(len(self.string1), len(self.string2), '', ''), ]
        results = []
        while True:
            i, j, s1, s2 = stack.pop()
            while i > 0 or j > 0:
                if len(self.dp[i][j].tracebacks) > 1:
                    stack.append((i, j, s1, s2))
                    ch = self.dp[i][j].tracebacks.pop()  # pop
                else:
                    ch = self.dp[i][j].tracebacks[0]  # peek

                if ch == NeedlemanWunsch.NORTH:
                    s2 += '-'
                    i -= 1
                    s1 += self.string1[i]
                elif ch == NeedlemanWunsch.NORTHWEST:
                    j -= 1
                    s2 += self.string2[j]
                    i -= 1
                    s1 += self.string1[i]
                else:
                    j -= 1
                    s2 += self.string2[j]
                    s1 += '-'
            results.append((s1[::-1], s2[::-1]))
            if onlyOne or not stack:
                return results

    def __prepare_matrix(self):
        for i, row in enumerate(self.dp):
            row[0].score = self.gap * i
            row[0].tracebacks.append(NeedlemanWunsch.NORTH)

        for i, cell in enumerate(self.dp[0]):
            cell.score = self.gap * i
            cell.tracebacks.append(NeedlemanWunsch.WEST)
