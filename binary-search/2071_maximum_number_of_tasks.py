from collections import deque
from typing import List


class Solution:
    def maxTaskAssign(
        self, tasks: List[int], workers: List[int], pills: int, strength: int
    ) -> int:
        # deque of tasks sorted: [weak ...   strong]
        # .                        ^popleft.  ^pop
        #                         ^use pill.  ^no pill needed
        # there are two operations we need to run on each task we iterate in sorted tasks
        #       Check if the strongest worker can do it without a pill
        #       if not, assign a pill to the weakest eligible worker

        def can_achieve(k) -> bool:
            """
            check if strongest workers can solve k easiest tasks and return true
            """
            t = tasks[:k]
            w = workers[-k:]
            dq = deque()
            remaining_p = pills
            # we process tasks from hardest
            # harder tasks have fewer valid capable workers
            # if we waste strong workers on easier tasks first, we get stuck later
            # we start with the first hardest task: k - 1, read again down to know why k - 1
            j = k - 1
            for i in range(k - 1, -1, -1):
                while j >= 0 and w[j] + strength >= t[i]:
                    dq.appendleft(w[j])
                    j -= 1
                if not dq:
                    return False
                if dq[-1] >= t[i]:
                    dq.pop()
                elif remaining_p > 0:
                    dq.popleft()
                    remaining_p -= 1
                else:
                    return False

            return True

        n = len(tasks)
        m = len(workers)
        tasks.sort()
        workers.sort()
        l, h, answer = 0, min(n, m), 0
        while l <= h:
            mid = (l + h) // 2
            if can_achieve(mid):
                answer = mid
                l = mid + 1
            else:
                h = mid - 1

        return answer
