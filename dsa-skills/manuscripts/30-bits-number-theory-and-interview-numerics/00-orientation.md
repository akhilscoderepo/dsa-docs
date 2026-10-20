<!-- section: orientation -->
## Orientation

A permissions service stores twelve yes-or-no flags per user in twelve separate booleans, and a million users cost a million small objects. A checksum routine adds two large counters and silently returns a negative total. A hash function multiplies two numbers and returns the wrong remainder. All three failures come from treating an integer as a plain number instead of a fixed row of 32 or 64 bits with exact rules.

### Prerequisites

You should know Java primitive types, loops and arrays, and the earlier chapters on hash maps, recursion and graph search. A bit is one binary digit, and an `int` holds 32 bits in two's complement form, so the top bit marks a negative value. Lesson 01 explains the operators `&`, `|`, `^` and `~` from scratch. Lesson 05 uses subsets of a small set, and the closing lesson uses breadth-first search from the graph chapters.

### The Ten Lessons

Each lesson answers one question about how Java stores and combines integers.

- **Bit Masks** store several flags in one integer and read, set, clear and flip them one at a time.
- **Shifts** move bits left or right, and they differ for negative values.
- **Low Bit** removes or isolates the lowest set bit, which counts bits in a loop that runs once per set bit.
- **XOR Cancellation** pairs equal values so that only the unpaired value remains.
- **Subset Masks** read every integer below a power of two as one subset.
- **Overflow** shows when `int` arithmetic wraps and how to widen or check first.
- **Binary Arithmetic** builds addition from XOR and carry.
- **GCD And Power** computes the greatest common divisor and repeated squaring.
- **Sieve** marks all composites up to a limit at once.
- **Modular Arithmetic** keeps results small with remainders that stay non-negative.

### The Closing Lesson

**Bits With Search State** stores a mask next to a search position, so one integer records which choices were made. Its exercises list subsets by size, find repeated fixed-width windows, pick the best pair of disjoint words and find a shortest walk that ends at a chosen node.

### How To Work Through Each Lesson

A lesson opens with a realistic failure. A short direct program follows, and you predict its behavior before the explanation appears. Later parts name the stored quantity and list the variables. Two traces, the code and the limits of the idea come after that. Each lesson states an invariant, which is a statement that stays true after every step of the loop. Four exercises close each lesson, and each has a hint and a solution that you can open after your own attempt.

### What You Can Do After This Chapter

You can pack and unpack flags, choose between signed and unsigned shifts, and count or isolate set bits. You can predict where `int` arithmetic wraps and pick `long` or an exact check. You can compute gcd, powers and prime tables, and you can keep remainders non-negative.
