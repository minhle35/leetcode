import importlib
import sys
import os
import pytest

# from 2071_maximum_number_of_tasks import Solution # syntax error : SyntaxError: invalid decimal literal

_module = importlib.import_module("2071_maximum_number_of_tasks")
# Solution = _module.Solution


@pytest.fixture
def sol():
    return _module.Solution()


def call(sol1, tasks, workers, pills, strength):
    return sol1.maxTaskAssign(tasks, workers, pills, strength)


# --- LeetCode official examples ---


# we can use @pytest with namespace mark and .parametrize decorator in the mark namespace
# parametrize will tell pytest to run the same test function multiple times, once per data row
# however, since there are no ways to visibily see the test name of each element -- test case
# this way of writing is a shortcut to quickly run some simple tests
# INSTEAD OF THIS, we should create a fixture, which is a factory that pytest calls automatically
# before each test. Any function that declares this fixture's function sol() as a parameter, for example
# def test_leetcode_example1(sol):
# will get a fresh Solution() instance injected by pytest, we never need to call the fixture by ourselves


# @pytest.mark.parametrize(
#     "tasks, workers, pills, strength, expected",
#     [
#         ([3, 2, 1], [0, 3, 3], 1, 1, 3),
#         ([5, 4], [0, 0, 0], 1, 5, 1),  # example 2
#         ([1, 2], [2], 0, 0, 1),  # worker reuse
#     ],
# )
# def test_max_task_assign(tasks, workers, pills, strength, expected):
#     assert _module.Solution().maxTaskAssign(tasks, workers, pills, strength) == expected


def test_leetcode_example1(sol):
    # Worker 0 takes pill (0+1=1>=1), worker 1 does task 2 (3>=2), worker 2 does task 3 (3>=3)
    assert call(sol, [3, 2, 1], [0, 3, 3], 1, 1) == 3


def test_leetcode_example2(sol):
    # Only one worker can be boosted to strength 5; no second task possible
    assert call(sol, [5, 4], [0, 0, 0], 1, 5) == 1


def test_leetcode_example3(sol):
    # Task 30 is unreachable (max boosted worker = 10+10 = 20 < 30); tasks 10 and 15 are doable
    assert call(sol, [10, 15, 30], [0, 10, 10, 10, 10], 3, 10) == 2


# --- Worker cannot be reused ---


def test_single_worker_two_distinct_tasks(sol):
    # Worker (strength 2) can satisfy both tasks individually, but can only be assigned once
    assert call(sol, [1, 2], [2], 0, 0) == 1


def test_single_worker_two_identical_tasks(sol):
    assert call(sol, [1, 1], [1], 0, 0) == 1


def test_three_workers_three_tasks_no_reuse(sol):
    # Each of the three workers can only serve one task
    assert call(sol, [1, 1, 1], [1, 1, 1], 0, 0) == 3


# --- Edge cases: empty inputs ---


def test_no_tasks(sol):
    assert call(sol, [], [1, 2, 3], 1, 1) == 0


def test_no_workers(sol):
    assert call(sol, [1, 2, 3], [], 1, 1) == 0


def test_no_tasks_no_workers(sol):
    assert call(sol, [], [], 0, 0) == 0


# --- Pill mechanics ---


def test_pill_provides_exact_needed_boost(sol):
    # 3 + 2 = 5 >= 5: pill makes it possible
    assert call(sol, [5], [3], 1, 2) == 1


def test_no_pill_worker_too_weak(sol):
    assert call(sol, [5], [3], 0, 2) == 0


def test_pill_boost_still_insufficient(sol):
    # 3 + 1 = 4 < 5: pill doesn't help enough
    assert call(sol, [5], [3], 1, 1) == 0


def test_worker_strong_enough_without_pill(sol):
    # Pill available but not needed
    assert call(sol, [5], [6], 1, 0) == 1


def test_all_workers_need_pills_enough_pills(sol):
    # Each worker needs a pill; exactly 3 pills available
    assert call(sol, [5, 5, 5], [3, 3, 3], 3, 2) == 3


def test_all_workers_need_pills_insufficient_pills(sol):
    # 3 workers need pills, only 2 available -> can complete 2 tasks
    assert call(sol, [5, 5, 5], [3, 3, 3], 2, 2) == 2


# --- Optimal pill assignment (greedy correctness) ---


def test_pill_must_go_to_weaker_worker_to_maximise(sol):
    # Suboptimal: pill on worker 6 -> 9>=7, but worker 4 can't do task 5 -> 1 task
    # Optimal:    pill on worker 4 -> 4+3=7>=7, worker 6 does task 5 (6>=5) -> 2 tasks
    assert call(sol, [5, 7], [4, 6], 1, 3) == 2


def test_should_skip_harder_task_to_complete_more_tasks(sol):
    # Best strategy: skip hardest task (20) and do two easier ones with pill help
    # workers [5, 8]: 5+5=10>=10, 8>=8 -> 2 tasks from [8, 10, 20]
    assert call(sol, [8, 10, 20], [5, 8], 1, 5) == 2


# --- Input ordering should not affect result ---


def test_unsorted_tasks(sol):
    assert call(sol, [3, 1, 2], [1, 2, 3], 0, 0) == 3


def test_unsorted_workers(sol):
    assert call(sol, [1, 2, 3], [3, 1, 2], 0, 0) == 3


def test_both_unsorted(sol):
    assert call(sol, [3, 1, 2], [3, 1, 2], 0, 0) == 3


# --- Worker/task count mismatches ---


def test_more_workers_than_tasks(sol):
    # Only 1 task to assign regardless of extra workers
    assert call(sol, [3], [1, 2, 3, 4, 5], 0, 0) == 1


def test_more_tasks_than_workers(sol):
    # Only 1 worker; it picks the easiest task it can handle
    assert call(sol, [1, 2, 3, 4, 5], [3], 0, 0) == 1


# --- All tasks impossible ---


def test_all_tasks_impossible_even_with_pills(sol):
    # Max boosted strength = 2 + 3 = 5 < 10; no task reachable
    assert call(sol, [10, 20], [1, 2], 2, 3) == 0


def test_zero_pills_and_all_workers_too_weak(sol):
    assert call(sol, [10], [5], 0, 0) == 0


# --- Perfect match ---


def test_exact_match_no_pills_needed(sol):
    assert call(sol, [1, 2, 3], [1, 2, 3], 0, 0) == 3


def test_single_task_single_worker_exact_strength(sol):
    assert call(sol, [5], [5], 0, 0) == 1
