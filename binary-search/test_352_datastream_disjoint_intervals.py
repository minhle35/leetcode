import importlib
import pytest

_module = importlib.import_module("352_datastream_disjoint_intervals")


@pytest.fixture
def sr():
    return _module.SummaryRanges()


def run_stream(obj, operations, args):
    """
    Simulates the LeetCode data-stream driver.
    obj is a SummaryRanges instance injected by the pytest fixture.
    Returns the list of outputs (None for void calls, result for getIntervals).
    """
    dispatch = {
        "SummaryRanges": lambda _: None,
        "addNum": lambda arg: (obj.addNum(*arg)) or None,
        "getIntervals": lambda _: obj.getIntervals(),
    }

    return [dispatch[op](arg) for op, arg in zip(operations, args)]


def check_stream(obj, operations, args, expected):
    outputs = run_stream(obj, operations, args)
    for i, (out, exp) in enumerate(zip(outputs, expected)):
        if exp is not None:
            assert out == exp, f"step {i} ({operations[i]}): got {out}, want {exp}"


# --- LeetCode official examples ---


def test_leetcode_example1(sr):
    check_stream(
        obj=sr,
        operations=[
            "SummaryRanges",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
        ],
        args=[[], [1], [], [3], [], [7], [], [2], [], [6], []],
        expected=[
            None,
            None,
            [[1, 1]],
            None,
            [[1, 1], [3, 3]],
            None,
            [[1, 1], [3, 3], [7, 7]],
            None,
            [[1, 3], [7, 7]],
            None,
            [[1, 3], [6, 7]],
        ],
    )


# --- Empty stream ---


def test_empty_stream(sr):
    check_stream(
        sr,
        ["SummaryRanges", "getIntervals"],
        [[], []],
        [None, []],
    )


# --- Single number ---


def test_single_number(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "getIntervals"],
        [[], [5], []],
        [None, None, [[5, 5]]],
    )


# --- Duplicates collapse into one interval ---


def test_duplicate_numbers(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "addNum", "getIntervals"],
        [[], [3], [3], []],
        [None, None, None, [[3, 3]]],
    )


# --- Sequential numbers merge ---


def test_merge_consecutive(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "addNum", "addNum", "getIntervals"],
        [[], [1], [2], [3], []],
        [None, None, None, None, [[1, 3]]],
    )


# --- Gap filled merges two intervals ---


def test_fill_gap_merges(sr):
    check_stream(
        sr,
        [
            "SummaryRanges",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
            "addNum",
            "getIntervals",
        ],
        [[], [1], [], [3], [], [2], []],
        [None, None, [[1, 1]], None, [[1, 1], [3, 3]], None, [[1, 3]]],
    )


# --- Numbers arriving in reverse order ---


def test_reverse_order(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "addNum", "addNum", "getIntervals"],
        [[], [5], [4], [3], []],
        [None, None, None, None, [[3, 5]]],
    )


# --- Multiple disjoint intervals, then bridged ---


def test_bridge_two_intervals(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "addNum", "getIntervals", "addNum", "getIntervals"],
        [[], [1], [3], [], [2], []],
        [None, None, None, [[1, 1], [3, 3]], None, [[1, 3]]],
    )


# --- Three separate intervals ---


def test_three_separate_intervals(sr):
    check_stream(
        sr,
        ["SummaryRanges", "addNum", "addNum", "addNum", "getIntervals"],
        [[], [1], [5], [10], []],
        [None, None, None, None, [[1, 1], [5, 5], [10, 10]]],
    )
