from typing import List


class Solution:
    def maxTaskAssign(
        self, tasks: List[int], workers: List[int], pills: int, strength: int
    ) -> int:
        max_tasks = 0
        used_worker = set()
        for i in range(len(tasks)):
            for j in range(len(workers)):
                if j in used_worker:
                    continue
                if workers[j] >= tasks[i]:
                    used_worker.add(j)
                    max_tasks += 1
                    break
                elif pills > 0 and strength + workers[j] >= tasks[i]:
                    used_worker.add(j)
                    pills -= 1
                    max_tasks += 1
                    break
        return max_tasks
