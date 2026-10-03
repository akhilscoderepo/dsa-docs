<!-- solutions-for: 02-fixed-frequency-windows -->
### Fixed Frequency Windows

#### Solution: [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-window-counts -->

**Approach.** Keep a table with one slot for `0` and one for `1`. When a character arrives, increase its slot. Once the window has more than `k` characters, decrease the slot of the character that left. When the window is full, read the number of ones directly from the table.

**Complexity.** O(n) time and O(1) extra space beyond the output array.

```java run
import java.util.Arrays;

public final class BinaryWindowCounts {
    static int[] onesPerBlock(String bits, int k) {
        int[] out = new int[bits.length() - k + 1];
        int[] count = new int[2];
        for (int right = 0; right < bits.length(); right++) {
            count[bits.charAt(right) - '0']++;
            if (right >= k) count[bits.charAt(right - k) - '0']--;
            if (right >= k - 1) out[right - k + 1] = count[1];
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(onesPerBlock("1101", 2), new int[] {2, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(onesPerBlock("000", 3), new int[] {0})) throw new AssertionError("example 2");
        if (!Arrays.equals(onesPerBlock("1", 1), new int[] {1})) throw new AssertionError("single");
    }
}
```

#### Solution: [Vary] Find All Anagrams in a String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Approach.** Build the probe's signature once. Slide a signature over `s`, adding the arriving letter and removing the departing one. Whenever the window is full and the two signatures are equal, record the start. If the probe is longer than the text there is no window, so return the empty list first.

**Complexity.** O(26 * n) time, which is O(n) for a fixed alphabet, and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class FindAnagrams {
    static List<Integer> findAnagrams(String s, String p) {
        List<Integer> starts = new ArrayList<>();
        int k = p.length();
        if (k > s.length()) return starts;
        int[] need = new int[26], have = new int[26];
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        for (int right = 0; right < s.length(); right++) {
            have[s.charAt(right) - 'a']++;
            if (right >= k) have[s.charAt(right - k) - 'a']--;
            if (right >= k - 1 && Arrays.equals(have, need)) starts.add(right - k + 1);
        }
        return starts;
    }

    public static void main(String[] args) {
        if (!findAnagrams("abacbabc", "abc").equals(List.of(1, 2, 3, 5))) throw new AssertionError("example 1");
        if (!findAnagrams("aaaa", "aa").equals(List.of(0, 1, 2))) throw new AssertionError("example 2");
        if (!findAnagrams("cbaebabacd", "abc").equals(List.of(0, 6))) throw new AssertionError("lesson trace");
        if (!findAnagrams("a", "ab").isEmpty()) throw new AssertionError("probe longer");
    }
}
```

#### Solution: [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Approach.** The probe's signature stores a count per letter, so the repeated `a` in `aab` requires a count of two in the window. Slide as before and return the first start at which the signatures are equal, or -1 after the scan. Check the length of the probe against the text first, and note that an empty text also falls out of that check.

**Complexity.** O(26 * n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class RepeatedRequired {
    static int firstRearrangement(String s, String p) {
        int k = p.length();
        if (k == 0 || k > s.length()) return -1;
        int[] need = new int[26], have = new int[26];
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        for (int right = 0; right < s.length(); right++) {
            have[s.charAt(right) - 'a']++;
            if (right >= k) have[s.charAt(right - k) - 'a']--;
            if (right >= k - 1 && Arrays.equals(have, need)) return right - k + 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (firstRearrangement("abbabb", "aab") != -1) throw new AssertionError("example 1");
        if (firstRearrangement("bbaab", "aab") != 1) throw new AssertionError("example 2");
        if (firstRearrangement("", "a") != -1) throw new AssertionError("empty text");
        if (firstRearrangement("aab", "aab") != 0) throw new AssertionError("whole text");
    }
}
```

#### Solution: [Recognize] Permutation in String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Approach.** This is the same signature window, but the answer is a Boolean. Return true at the first full window whose signature equals that of `s1`, and return false if the scan ends. A longer `s1` than `s2` means no window can exist.

**Complexity.** O(26 * n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class PermutationInString {
    static boolean checkInclusion(String s1, String s2) {
        int k = s1.length();
        if (k > s2.length()) return false;
        int[] need = new int[26], have = new int[26];
        for (int i = 0; i < k; i++) need[s1.charAt(i) - 'a']++;
        for (int right = 0; right < s2.length(); right++) {
            have[s2.charAt(right) - 'a']++;
            if (right >= k) have[s2.charAt(right - k) - 'a']--;
            if (right >= k - 1 && Arrays.equals(have, need)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!checkInclusion("abc", "xxcabyy")) throw new AssertionError("example 1");
        if (checkInclusion("abc", "acxbcxa")) throw new AssertionError("example 2");
        if (checkInclusion("abc", "ab")) throw new AssertionError("longer probe");
        if (!checkInclusion("a", "a")) throw new AssertionError("single letters");
    }
}
```
