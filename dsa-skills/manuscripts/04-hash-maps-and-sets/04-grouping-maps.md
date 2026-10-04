<!-- lesson-kind: standard -->
<!-- lesson-id: grouping-maps -->
## Group Values In A Map

<!-- stage: context -->
### Sending Jobs To Worker Queues

A scheduler receives up to 100000 job numbers, and it sends job `v` to worker `v mod m`, where `m` is the number of workers. Each worker needs its own list of jobs, in the order the jobs arrived. The scheduler must also skip workers that received no job. The first version of the scheduler works with ten workers. With a million possible workers it spends most of its time on workers that have nothing to do.

The task is to split one sequence into lists, where all values in a list share a property. The question is how the program collects each list in one pass, and how it avoids all work for lists that stay empty.

<!-- stage: naive -->
### Scanning All Jobs For Each Worker

The direct method visits each worker number from 0 to `m - 1`. For each worker it scans all jobs and collects the jobs that belong to the worker. It keeps a list only if the worker received a job.

```java
static List<List<Integer>> groupJobs(int[] jobs, int m) {
    List<List<Integer>> result = new ArrayList<>();
    for (int worker = 0; worker < m; worker++) {
        List<Integer> mine = new ArrayList<>();
        for (int job : jobs) {
            if (Math.floorMod(job, m) == worker) {
                mine.add(job);
            }
        }
        if (!mine.isEmpty()) {
            result.add(mine);
        }
    }
    return result;
}
```

On `[9, 4, 6, 1, -2]` with `m = 3` the method returns `[[9, 6], [4, 1, -2]]`. The call `Math.floorMod(job, m)` returns a value from 0 to `m - 1` even for a negative job number.

<!-- stage: bottleneck -->
### Every Worker Scans Every Job

```predict
There are 100000 jobs and m = 100000 workers, and the jobs use only 3 distinct workers. About how many job inspections does the method make, and how many of them are useful?

The method makes about m * n = 10 billion inspections, which is O(m * n). Only 100000 of them matter, one per job, because each job belongs to exactly one worker. The other inspections test a job against a worker it does not belong to.
```

Each job belongs to exactly one worker, and the method still tests it against all `m` workers. The answer for a job, namely its worker number, takes one computation. The method repeats a search where one computation would do. The program only needs to read each job once, compute its worker, and append the job to that worker's list. The lists should exist only for workers that receive a job, so the work depends on the number of jobs and not on `m`.

<!-- stage: insight -->
### Collect Values Under A Group Key

#### Compute A Group Key For Each Value

Two values are in the same group when they have the same result under a fixed rule. The result of the rule is the **group key**. Here the rule is `Math.floorMod(job, m)`. The rule splits the input into groups, with each value in exactly one group, which is the standard way an equivalence relation partitions a set.

<!-- names: grouping map, group key, bucket -->

#### Keep One Bucket For Each Key

A **grouping map** is a map from a group key to the list of all values that have that key. Each list is a **bucket**. Java's type is `Map<Integer, List<Integer>>`. A frequency map stores only how many values a key has, so it cannot return the members. The grouping map stores the members themselves.

#### Create A Bucket When The First Value Arrives

The call `groups.computeIfAbsent(key, k -> new ArrayList<>())` returns the bucket of the key. When the key has no bucket, the call creates an empty one first. The loop then appends the value, so `computeIfAbsent(key, ...).add(v)` handles both cases in one line. Buckets exist only for keys that received a value, so the map never holds an empty bucket, and its size is the number of non-empty groups.

#### The Invariant Of The Pass

After the iteration for index `i`, `groups.get(key)` holds exactly the values of `jobs[0..i]` whose key equals `key`, in the order of arrival. The pass costs O(n) on average, because each job needs one key computation and one append. The map holds all n values in its buckets, so the space is O(n).

<!-- stage: variables -->
### Key, Map And Bucket

Each iteration of the pass uses three values.

- **key** equals `Math.floorMod(jobs[i], m)` and changes with every job.
- **groups** maps each key that occurred to its bucket and gains an entry when a key appears for the first time.
- **bucket** is the list that `groups` holds for `key`, and the loop appends `jobs[i]` to it.

<!-- stage: trace -->
### Filling Buckets From Two Job Lists

#### Jobs With Negative Numbers

Take `jobs = [7, -1, 4, 2, 10, 5]` and `m = 3`. The job 7 has key 1, so the loop creates a bucket for key 1 and adds 7. The job -1 has key `floorMod(-1, 3) = 2`, so the loop creates a bucket for key 2. The jobs 4 and 10 join the bucket of key 1, and the jobs 2 and 5 join the bucket of key 2. The final map holds key 1 with `[7, 4, 10]` and key 2 with `[-1, 2, 5]`.

#### A Key That Comes Back Later

Now take `jobs = [8, 3, 12, 5, 4]` and `m = 4`. The keys are 0, 3, 0, 1 and 0. The loop creates the bucket for key 0 first. That bucket receives 12 at index 2 and 4 at index 4. The final map holds key 0 with `[8, 12, 4]`, key 3 with `[3]` and key 1 with `[5]`. A bucket for key 2 never exists, because no job has key 2.

#### Stepping Through Both Lists

```trace
{"cells":[7,-1,4,2,10,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"groups":"{}"},"note":"Start: the grouping map is empty."},{"at":{"i":0},"vars":{"job":7,"key":1,"groups":"{1: [7]}"},"note":"Job 7 has key 1, which has no bucket yet. Create the bucket and add the job."},{"at":{"i":1},"vars":{"job":-1,"key":2,"groups":"{1: [7], 2: [-1]}"},"note":"Job -1 has key 2, which has no bucket yet. Create the bucket and add the job."},{"at":{"i":2},"vars":{"job":4,"key":1,"groups":"{1: [7, 4], 2: [-1]}"},"note":"Job 4 has key 1. Append it to the existing bucket."},{"at":{"i":3},"vars":{"job":2,"key":2,"groups":"{1: [7, 4], 2: [-1, 2]}"},"note":"Job 2 has key 2. Append it to the existing bucket."},{"at":{"i":4},"vars":{"job":10,"key":1,"groups":"{1: [7, 4, 10], 2: [-1, 2]}"},"note":"Job 10 has key 1. Append it to the existing bucket."},{"at":{"i":5},"vars":{"job":5,"key":2,"groups":"{1: [7, 4, 10], 2: [-1, 2, 5]}"},"note":"Job 5 has key 2. Append it to the existing bucket."}]}
```

```trace
{"cells":[8,3,12,5,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"groups":"{}"},"note":"Start: the grouping map is empty."},{"at":{"i":0},"vars":{"job":8,"key":0,"groups":"{0: [8]}"},"note":"Job 8 has key 0, which has no bucket yet. Create the bucket and add the job."},{"at":{"i":1},"vars":{"job":3,"key":3,"groups":"{0: [8], 3: [3]}"},"note":"Job 3 has key 3, which has no bucket yet. Create the bucket and add the job."},{"at":{"i":2},"vars":{"job":12,"key":0,"groups":"{0: [8, 12], 3: [3]}"},"note":"Job 12 has key 0. Append it to the existing bucket."},{"at":{"i":3},"vars":{"job":5,"key":1,"groups":"{0: [8, 12], 3: [3], 1: [5]}"},"note":"Job 5 has key 1, which has no bucket yet. Create the bucket and add the job."},{"at":{"i":4},"vars":{"job":4,"key":0,"groups":"{0: [8, 12, 4], 3: [3], 1: [5]}"},"note":"Job 4 has key 0. Append it to the existing bucket."}]}
```

<!-- stage: code -->
### One Pass With A Grouping Map

#### Building The Buckets

```java
static List<List<Integer>> groupJobs(int[] jobs, int m) {
    Map<Integer, List<Integer>> groups = new LinkedHashMap<>();
    for (int job : jobs) {
        int key = Math.floorMod(job, m);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(job);
    }
    return new ArrayList<>(groups.values());
}
```

#### What The Method Costs

Across n iterations, the loop computes one key, makes one map operation and one append. The expected total time is O(n). The buckets together hold n values, so the space is O(n). The method does not depend on `m`, so a value of `m` near one billion costs nothing extra. A `LinkedHashMap` returns the buckets in the order in which their keys first appeared. The method with one scan for each worker lists groups by worker number instead, so the two orders can differ, and each exercise states the order it needs.

<!-- stage: applicability -->
### When A Map Of Lists Fits

#### Look For An Equivalence Rule

Use a grouping map when several inputs belong to one output bucket under a stated rule, and the output must keep the members. Typical rules are the remainder of a division, the length of a word, or a computed signature of a word. The invariant is that `groups.get(key)` holds the complete list of one equivalence class, and the list order follows the input order. The rule must read the value alone. Equal values then always receive equal keys.

#### A Frequency Map Is A False Friend

A false friend here is a frequency map. A frequency map tells how many values share a key, and it cannot return them. If the output is a list of members, counting does not suffice. If the question asks only how many values fall in each class, a frequency map is the simpler and cheaper choice, since it stores one number per key.

#### Java Details That Cause Failures

The operator `%` returns a negative result for a negative left operand, so `-1 % 3` is -1 and the key would fall outside the range 0 to 2. Use `Math.floorMod`. Create each bucket on demand with `computeIfAbsent`, and do not allocate buckets for all possible keys, since that costs time and memory in proportion to `m`. A `HashMap` makes no promise about the order of its keys, so a result that must follow the order of first appearance needs `LinkedHashMap`.

<!-- stage: exercises -->
### Exercises

#### [Build] Group By Remainder (Author exercise)
<!-- id: hm-group-by-remainder -->

**Prerequisites.** The grouping map and the on-demand bucket from this lesson.

**Problem.** Let `nums` be an integer array and `m` a positive integer. Group the values by the key `Math.floorMod(value, m)`. Return the groups as a list of lists. List the groups in the order in which their keys first appear, and list the values of a group in input order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, and negative values are legal.
- **Modulus** satisfies `1 <= m <= 10^9`.
- **Answer** holds no empty list.

**Example 1.** Input `nums = [9, 4, 6, 1, -2]`, `m = 3`, output `[[9, 6], [4, 1, -2]]`.

**Example 2.** Input `nums = []`, `m = 5`, output `[]`.

**Hint.** What does the loop compute for each value, and what must exist before the loop appends the value?

**Changed decision.** Basic case: a map from key to list replaces one scan per key.

#### [Vary] Group The People By Group Size (LeetCode 1282)
<!-- id: hm-group-people -->

**Prerequisites.** Group By Remainder above.

**Problem.** Let `sizes` be an integer array in which `sizes[i]` is the size of the group that person `i` must belong to. Return a partition of the persons `0` to `n - 1` into groups, where every group of person `i` has exactly `sizes[i]` members. List the groups in the order in which they become full, and list members in increasing order. A valid partition exists.

**Constraints.** The limits are:
- **Length** satisfies `1 <= sizes.length <= 500`.
- **Sizes** satisfy `1 <= sizes[i] <= sizes.length`.
- **Validity** guarantees that a partition exists.
- **Answer** emits a group when it reaches its required size.

**Example 1.** Input `sizes = [2, 1, 2, 3, 3, 3]`, output `[[1], [0, 2], [3, 4, 5]]`.

**Example 2.** Input `sizes = [1, 1]`, output `[[0], [1]]`.

**Hint.** Which key names the group that is still filling, and when does the program remove it from the map?

**Changed decision.** A bucket is a group under construction, and the program emits it and removes it when it is full.

#### [Boundary] Empty Buckets (Author exercise)
<!-- id: hm-empty-buckets -->

**Prerequisites.** The two exercises above and the on-demand bucket from this lesson.

**Problem.** Take an integer array `nums` and a positive modulus `m`. Group the values by `Math.floorMod(value, m)`. Return the sizes of the non-empty groups, in the order in which their keys first appear.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers.
- **Modulus** satisfies `1 <= m <= 10^9`, so the program cannot allocate one bucket per possible key.
- **Answer** holds one entry for each key that received a value.

**Example 1.** Input `nums = [10, 20, 31, 41, 51]`, `m = 10`, output `[2, 3]`.

**Example 2.** Input `nums = []`, `m = 7`, output `[]`.

**Hint.** If the program created a bucket for each of the `m` keys at the start, what would that cost when `m` is large?

**Changed decision.** A key without values must not exist in the map, so every bucket comes from demand.

#### [Recognize] Group Anagrams (LeetCode 49)
<!-- id: hm-group-anagrams -->

**Prerequisites.** All three exercises above and the letter table from Chapter 03.

**Problem.** Let `words` be an array of strings of lowercase letters. Two words are in the same group when one is a rearrangement of the other. Return the groups. List the groups in the order in which their first word appears, and list words in input order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= words.length <= 10^4`, and each word has at most 100 letters.
- **Characters** are the lowercase letters `'a'` to `'z'`.
- **Words** may be empty, and equal words stay in the same group.
- **Key** is a string built from the 26 letter counts, not from sorting.

**Example 1.** Input `words = ["stop", "pots", "cat", "tops", "act", "dog"]`, output `[["stop", "pots", "tops"], ["cat", "act"], ["dog"]]`.

**Example 2.** Input `words = [""]`, output `[[""]]`.

**Hint.** Which value is equal for every rearrangement of a word, and how can the program turn it into a map key?

**Changed decision.** The key is a computed signature of the word, and the map owns one bucket for each signature.
