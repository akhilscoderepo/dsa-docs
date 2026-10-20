<!-- section: orientation -->
## Orientation

A shop changes the price of a product. The product page shows the new price, and the sorted category page still shows the old one. Nothing crashed, and every structure holds data that was true a moment ago. The service is wrong because one record lives in two places and an update reached only one of them.

This chapter teaches classes in which one logical record appears in several indexes at once: a lookup by id, a ranking, a set of free resources, a count group or a price order. Each lesson asks which copy is the source of truth, which indexes follow it, and which step repairs them together.

### Prerequisites

You should know hash maps, tree sets and tree maps, priority queues, doubly linked lists and the cache designs of chapter 33. A **secondary index** is a structure that holds the same facts as the main record in another order. A **stale entry** is an index entry that no longer matches the record. An **invariant** is a statement that every call must leave true. A **call** is one public method of a class, and the **workload** is the mix of calls the class must serve.

### What Each Lesson Protects

Each lesson names a fact that every call must leave true.

- **Multi-Index Records** keeps the main record and every secondary index describing the same live entities.
- **Dynamic Rankings** keeps the order total, so no two entries tie and an update removes the exact old key.
- **Resource Allocation** keeps free and taken resources as two sets with no overlap.
- **Frequency Buckets** keeps every key in the one bucket that matches its count.
- **Validated Priority** keeps the heap as a list of candidates that the record can reject.
- **Transaction Lifecycles** keeps each call all-or-nothing across every index.
- **Look Up By ID And By Order** joins the record map with sorted views that have several exits.
- **Pick The Best Free Resource** joins free resources with candidates whose priority comes from neighbors.

### Reading Order

Every lesson opens with a class that passes small tests and fails under a real workload. You predict the failure before the explanation. Two traces follow the state call by call. The last parts show the Java code and the places where the idea fails. The four exercises run from a basic build, through a variation and an edge case, to a problem you must recognize. A **false friend** is a design that mimics the pattern and breaks one of its conditions. The solutions check each class against a slow, obviously correct version on random calls. The two closing lessons add a section that names what each earlier lesson contributes.

### What You Can Do After This Chapter

You can list every index that a public call must touch before writing the call. You can choose between exact removal from a sorted set and a version check on a heap. You can split a call into a plan that only reads and a commit that cannot fail. The lock-free and cache designs belong to other chapters.
