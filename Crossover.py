import numpy as np
from collections import defaultdict


class Crossover:
    @staticmethod
    def pmx_crossover(par_1, par_2):
        l = par_1.shape[0]

        child_1 = np.full_like(par_1, -1)
        child_2 = np.full_like(par_2, -1)

        used_1 = np.full_like(par_1, False)
        used_2 = np.full_like(par_2, False)

        i, j = np.random.choice(range(l), 2, replace=False)

        if i > j:
            i, j = j, i

        i, j = 3, 6
        child_1[i:j+1] = par_1[i:j+1]
        child_2[i:j+1] = par_2[i:j+1]

        for q in range(i, j+1):
            used_1[par_2[q]] = True
            used_2[par_1[q]] = True

        for q in range(i, j+1):
            if not used_2[par_2[q]]:
                p = q
                while child_1[p] != -1:
                    p = np.where(par_2 == child_1[p])[0]
                child_1[p] = par_2[q]

            if not used_1[par_1[q]]:
                p = q
                while child_2[p] != -1:
                    p = np.where(par_1 == child_2[p])[0]
                child_2[p] = par_1[q]

        for q in range(l):
            if i <= q and q <= j:
                continue

            if child_1[q] == -1:
                child_1[q] = par_2[q]

            if child_2[q] == -1:
                child_2[q] = par_1[q]

        return [child_1, child_2]

    @staticmethod
    def edge_crossover(par_1, par_2):
        l = par_1.shape[0]

        edge_table = defaultdict(list)

        edge_table[par_1[0].item()].append(par_1[-1].item())
        edge_table[par_1[0].item()].append(par_1[1].item())
        edge_table[par_2[0].item()].append(par_2[-1].item())
        edge_table[par_2[0].item()].append(par_2[1].item())

        edge_table[par_1[-1].item()].append(par_1[-2].item())
        edge_table[par_1[-1].item()].append(par_1[0].item())
        edge_table[par_2[-1].item()].append(par_2[-2].item())
        edge_table[par_2[-1].item()].append(par_2[0].item())
        for i in range(1, l-1):
            edge_table[par_1[i].item()].append(par_1[i-1].item())
            edge_table[par_1[i].item()].append(par_1[i+1].item())
            edge_table[par_2[i].item()].append(par_2[i-1].item())
            edge_table[par_2[i].item()].append(par_2[i+1].item())

        # for k in edge_table:
        #     edge_table[k].sort()

        child = np.zeros_like(par_1)
        used = np.full_like(par_1, False)
        q = np.random.randint(l, size=1).item()
        child[0] = q
        used[q] = True

        for i in range(1, l):
            done = False
            for j in edge_table[q]:
                if used[j]:
                    continue

                if edge_table[q].count(j) > 1:
                    q = j
                    child[i] = q
                    used[q] = True
                    done = True
                    break

            if not done:
                for j in edge_table[q]:
                    if used[j]:
                        continue

                    q = j
                    child[i] = q
                    used[q] = True
                    done = True
                    break

            if not done:
                q = np.random.choice(np.where(used == False)[0], 1).item()
                child[i] = q
                used[q] = True

        return [child]

    @staticmethod
    def order_crossover(par_1, par_2):
        l = par_1.shape[0]

        child_1 = np.zeros_like(par_1)
        child_2 = np.zeros_like(par_2)

        used_1 = np.full_like(par_1, False)
        used_2 = np.full_like(par_2, False)

        i, j = np.random.choice(range(l), 2, replace=False)

        if i > j:
            i, j = j, i

        child_1[i:j+1] = par_1[i:j+1]
        child_2[i:j+1] = par_2[i:j+1]

        for k in range(i, j+1):
            used_1[par_2[k]] = True
            used_2[par_1[k]] = True

        q_1 = (j+1 if j < l-1 else 0)
        q_2 = (j+1 if j < l-1 else 0)
        for k in range(j+1, l):
            if not used_2[par_2[k]]:
                used_2[par_2[k]] = True
                child_1[q_1] = par_2[k]
                q_1 += 1
                if q_1 >= l:
                    q_1 = 0

            if not used_1[par_1[k]]:
                used_1[par_1[k]] = True
                child_2[q_2] = par_1[k]
                q_2 += 1
                if q_2 >= l:
                    q_2 = 0

        for k in range(0, j+1):
            if not used_2[par_2[k]]:
                used_2[par_2[k]] = True
                child_1[q_1] = par_2[k]
                q_1 += 1
                if q_1 >= l:
                    q_1 = 0

            if not used_1[par_1[k]]:
                used_1[par_1[k]] = True
                child_2[q_2] = par_1[k]
                q_2 += 1
                if q_2 >= l:
                    q_2 = 0

        return [child_1, child_2]

    @staticmethod
    def cycle_crossover(par_1, par_2):
        l = par_1.shape[0]

        position = np.zeros_like(par_1)
        for i in range(l):
            position[par_1[i]] = i

        used = np.full_like(par_1, False)
        child_1 = np.copy(par_1)
        child_2 = np.copy(par_2)

        swap = False
        for i in range(l):
            if used[i]:
                continue

            used[i] = True
            if swap:
                child_1[i], child_2[i] = child_2[i], child_1[i]

            cycle = [i]
            j = position[par_2[i]]
            while j != i:
                cycle.append(j)
                used[j] = True
                if swap:
                    child_1[j], child_2[j] = child_2[j], child_1[j]

                j = position[par_2[j]]

            swap = not swap

        return [child_1, child_2]


if __name__ == "__main__":

    parent1 = np.random.permutation(10)
    parent2 = np.random.permutation(10)
    print(parent1, parent2)
    child1 = Crossover.pmx_crossover(parent1, parent2)
    print(child1)
