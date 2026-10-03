<!-- section: unlocked-combinations -->
## Unlocked Combinations

Every ingredient of one combination has now been taught, so it has a lesson of its own and a separate four-rung ladder. A second combination is recorded as deferred, with the chapter that will supply what it still lacks.

### Teach Now

The linked list together with the hash map is the eleventh lesson. The list supplies the identity of every node and a single route through all of them, and the map supplies a direct lookup from an original node to its copy. Together they allow a structure whose nodes point at each other arbitrarily to be duplicated in two passes: all copies first, all links second. The ladder goes from the map alone, through the standard copy with a random reference, to a case of null, self and shared targets, and ends with a node that has two arbitrary references. The false friend is a map keyed by value, which quietly merges nodes that merely look alike.

### Deferred

A cache that evicts the entry used longest ago needs a map for lookup and a doubly linked recency list with guard nodes at both ends. The list operations needed are already available from this chapter, but the design of the cache interface, its operations and its eviction contract belongs to Chapter 33. No cache problem is assigned here.

### Already Covered

Hash maps keyed by value or by object were taught in Chapter 04, and the idea that the key must be chosen to match the question is used here without being taught again. Merging two ordered sequences and the idea of a stable choice on ties were prepared in Chapter 05. Pointer movement with an invariant, the model for every lesson in this chapter, comes from Chapter 08, and the argument that each node is visited a constant number of times follows the sliding window argument of Chapter 09.
