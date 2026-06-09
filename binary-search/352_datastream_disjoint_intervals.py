"""_summary_
Given a data stream input of non-negative integers a1, a2, ..., an, summarize the numbers seen so far as a list of disjoint intervals.

Implement the SummaryRanges class:

SummaryRanges() Initializes the object with an empty stream.
void addNum(int value) Adds the integer value to the stream.
int[][] getIntervals() Returns a summary of the integers in the stream currently as a list of disjoint intervals [starti, endi]. The answer should be sorted by starti.
"""

from typing import List


class SummaryRanges:
    def __init__(self):
        self._data = []

    def _bs(self, value):
        left = 0
        right = len(self._data) - 1
        while left <= right:
            mid = (left + right) // 2

            if self._data[mid] < value:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def addNum(self, value: int) -> None:
        self._data.insert(self._bs(value), value)

    def _find_consecutive_groups(self) -> List[List[int]]:
        """Return a list of [start, end] intervals for each consecutive group."""
        if not self._data:
            return []
        groups = []
        left = 0
        for right in range(1, len(self._data)):
            if self._data[right] > self._data[right - 1] + 1:
                groups.append([self._data[left], self._data[right - 1]])
                left = right
        groups.append([self._data[left], self._data[-1]])
        return groups

    def getIntervals(self) -> List[List[int]]:
        return self._find_consecutive_groups()


# Your SummaryRanges object will be instantiated and called as such:
# obj = SummaryRanges()
# obj.addNum(value)
# param_2 = obj.getIntervals()

if __name__ == "__main__":
    sr = SummaryRanges()
    sr.addNum(1)
    sr.addNum(2)
    sr.addNum(3)
    sr.addNum(5)
    sr.addNum(6)
    groups = sr._find_consecutive_groups()
    for i in groups:
        print(i)
