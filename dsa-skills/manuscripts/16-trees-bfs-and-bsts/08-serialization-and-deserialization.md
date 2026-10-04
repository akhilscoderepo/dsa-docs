<!-- lesson-kind: standard -->
<!-- lesson-id: serialization-and-deserialization -->
## Serialization And Deserialization

<!-- stage: context -->
### Posting A Hanging Mobile

A craftsman makes hanging mobiles: a rod holds a weight, and from each end of a rod another weight may hang, with its own rods below, and so on down. A customer overseas wants a copy, and the shop cannot ship a mobile through the post. It can send a plain card with writing on it, and the customer will rebuild the mobile from the card with the right weights in exactly the right places.

The craftsman wonders what has to be written on the card. Weights alone are surely not enough, since the same set of weights can be hung in many different shapes. Whatever he writes, the customer must be able to follow it from the first line to the last and end up with the same mobile, without any chance to ask a question.

<!-- stage: naive -->
### A Slot For Every Possible Position

The craftsman can draw an imaginary full frame in which every weight has two possible places below it, so that position i has its two places at 2i+1 and 2i+2. He writes one line per place of the frame, either a weight or the word empty, down to the lowest weight he has. The customer reads the frame back the same way, and the shape is fixed by which places are filled.

```java
static String[] byFrame(Node root, int height) {
    String[] card = new String[(1 << height) - 1];
    Arrays.fill(card, "empty");
    fill(root, 0, card);
    return card;
}

static void fill(Node node, int place, String[] card) {
    if (node == null) return;
    card[place] = String.valueOf(node.val);
    fill(node.left, 2 * place + 1, card);
    fill(node.right, 2 * place + 2, card);
}
```

The shape is exactly recoverable, because a filled place always has its parent at (place - 1) / 2, and the card contains every weight.

<!-- stage: bottleneck -->
### The Frame Doubles With Every Level

A frame for a mobile of height h has 2^h - 1 places, whatever the number of weights. A mobile of n = 30 weights hung in a single chain has a height of 30, so the card has over a billion lines, and almost all of them say empty. In general the card costs O(2^h) lines for a tree of n nodes, which is O(2^n) in the worst case. Nobody can post that, and the sender cannot even write it.

The waste comes from describing places beneath places that do not exist. An empty place has nothing below it, so only one line is ever needed for it. If the card spent one line per weight and one line per missing hanging spot directly under an existing weight, the total would be n weights plus n + 1 empty spots, which is 2n + 1 lines and O(n). The remaining question is how the customer knows how the lines fit together without any frame positions.

<!-- stage: insight -->
### Write Down A Walk With Markers

Write the mobile by a walk that the customer can repeat: take the weight, then write the whole left hanging, then the whole right hanging. Wherever a hanging spot is empty, write a **null marker** such as `#`. This is the preorder walk with explicit emptiness, and for a mobile of n weights the card has exactly 2n + 1 tokens.

The customer reads the card with the same walk turned around. Read a token. If it is the marker, the spot is empty. Otherwise create a weight, then build its left hanging by reading as many tokens as the left hanging needs, and then its right hanging the same way. This works because the writer and the reader follow a **shared grammar**: a hanging is either a marker, or a weight followed by two hangings. The reader never needs to be told how long a hanging is, since the markers tell it when each one ends.

The reader needs a single **token cursor** that moves forward exactly once per token, and every recursive call must leave it just after the tokens that its subtree used.

The invariant is that when a call starts, the cursor stands on the first token of the subtree it must build, and when it returns, the cursor stands on the first token after that subtree's last one.

<!-- names: null marker, shared grammar, token cursor -->

Without the markers two different shapes can produce the same card, so dropping them loses information, not just space.

<!-- stage: variables -->
### Builder, Tokens And Cursor

The encoder owns a `StringBuilder` that grows by one token at each visited position and is never read until the end. The decoder owns a `String[] tokens` produced by splitting the text at the delimiter, which must be a character that cannot occur inside a number, such as a comma. The `cursor` is an int that must be shared by all recursive calls, so it lives in a one-element array or a field and not in a parameter, because a parameter would be copied on each call and the parent would not see how far the child read. Removing tokens from the front of a list for each read is a hazard, since `ArrayList.remove(0)` shifts every remaining element and turns the decoder quadratic.

<!-- stage: trace -->
### Writing And Reading One Mobile

The first trace writes the mobile 1, 2, 3, null, null, 4, 5 by preorder. The marker `node` rests on the position currently being written, and `card` shows the text produced so far. A weight writes its value and then its two hangings, so the empty positions under the weight 2 write one marker each, and the leaf weights 4 and 5 write both markers in their own step because their empty hangings are not listed in the array.

```trace
{"cells":["1","2","3","null","null","4","5"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"card":"1"},"note":"The weight 1 is written first, and its left hanging and then its right hanging follow."},{"at":{"node":1},"vars":{"card":"1,2"},"note":"The weight 2 is written first, and its left hanging and then its right hanging follow."},{"at":{"node":3},"vars":{"card":"1,2,#"},"note":"This hanging spot is empty, so one marker # is written for it."},{"at":{"node":4},"vars":{"card":"1,2,#,#"},"note":"This hanging spot is empty, so one marker # is written for it."},{"at":{"node":2},"vars":{"card":"1,2,#,#,3"},"note":"The weight 3 is written first, and its left hanging and then its right hanging follow."},{"at":{"node":5},"vars":{"card":"1,2,#,#,3,4,#,#"},"note":"The weight 4 is a leaf with no cells below it, so it is written and then two markers # for its empty hangings."},{"at":{"node":6},"vars":{"card":"1,2,#,#,3,4,#,#,5,#,#"},"note":"The weight 5 is a leaf with no cells below it, so it is written and then two markers # for its empty hangings."}]}
```

The second trace reads the finished card 1, 2, #, #, 3, 4, #, #, 5, #, # back into a mobile. Here the cells are the tokens themselves and the marker `cursor` stands on the token being read. The note for each step says which weight is created or which empty spot is closed. The reader never looks ahead, and the order in which the left and right hangings get filled follows the same walk that wrote the card.

```trace
{"cells":["1","2","#","#","3","4","#","#","5","#","#"],"pointers":["cursor"],"steps":[{"at":{"cursor":0},"vars":{"building":"1"},"note":"The token 1 creates the weight 1 as the root, and its left hanging is read next."},{"at":{"cursor":1},"vars":{"building":"2"},"note":"The token 2 creates the weight 2 as the left child of 1, and its left hanging is read next."},{"at":{"cursor":2},"vars":{"building":"2"},"note":"The marker # closes an empty left hanging of 2."},{"at":{"cursor":3},"vars":{"building":"2"},"note":"The marker # closes an empty right hanging of 2."},{"at":{"cursor":4},"vars":{"building":"3"},"note":"The token 3 creates the weight 3 as the right child of 1, and its left hanging is read next."},{"at":{"cursor":5},"vars":{"building":"4"},"note":"The token 4 creates the weight 4 as the left child of 3, and its left hanging is read next."},{"at":{"cursor":6},"vars":{"building":"4"},"note":"The marker # closes an empty left hanging of 4."},{"at":{"cursor":7},"vars":{"building":"4"},"note":"The marker # closes an empty right hanging of 4."},{"at":{"cursor":8},"vars":{"building":"5"},"note":"The token 5 creates the weight 5 as the right child of 3, and its left hanging is read next."},{"at":{"cursor":9},"vars":{"building":"5"},"note":"The marker # closes an empty left hanging of 5."},{"at":{"cursor":10},"vars":{"building":"5"},"note":"The marker # closes an empty right hanging of 5."}]}
```

<!-- stage: code -->
### A Matched Encoder And Decoder

```java
final class TreeCodec {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static String serialize(Node root) {
        StringBuilder card = new StringBuilder();
        write(root, card);
        return card.toString();
    }

    private static void write(Node node, StringBuilder card) {
        if (node == null) { card.append("#,"); return; }
        card.append(node.val).append(',');
        write(node.left, card);
        write(node.right, card);
    }

    static Node deserialize(String text) {
        String[] tokens = text.split(",");
        int[] cursor = {0};
        return read(tokens, cursor);
    }

    private static Node read(String[] tokens, int[] cursor) {
        String token = tokens[cursor[0]++];
        if (token.equals("#")) return null;
        Node node = new Node(Integer.parseInt(token));
        node.left = read(tokens, cursor);
        node.right = read(tokens, cursor);
        return node;
    }
}
```

The encoder writes 2n + 1 tokens and the decoder reads each token once, so both take O(n) time. The extra space is the text itself, O(n), plus the recursion depth O(h), which reaches n for a chain.

<!-- stage: applicability -->
### When A Tree Must Cross A Boundary

Use a matched encoder and decoder whenever a tree must be saved to a file, sent over a network, or stored in a text column: a decision tree stored by a service, a cached search index, or a test fixture. The invariant is that the encoder and decoder follow the same grammar, so each recursive call reads exactly the tokens its counterpart wrote.

The first false friend is the card of values alone, even in a visit order such as preorder. Two different shapes can produce the same list of values, so the reader has no way to decide what belongs on the left. A second false friend is a delimiter-free number string, in which the weights 1 and 12 followed by 3 are indistinguishable from 11 followed by 23. A third is the frame layout of the naive approach, which is correct but costs O(2^h).

In Java, avoid `ArrayList.remove(0)` for reading tokens and use a moving index. Avoid a marker such as `-` or a digit, which could be confused with a value, and remember that `Integer.parseInt` on a token like `-10` is fine but on an empty string throws. A chain of a hundred thousand nodes would overflow the call stack in both recursive routines, so deep inputs need the level-by-level form with a queue.

<!-- stage: exercises -->
### Exercises

#### [Build] Preorder With Null Markers (Author exercise)
<!-- id: tb-preorder-null-markers -->

**Prerequisites.** The tree DFS chapter and the preorder walk.

**Problem.** A tree arrives in level-order array form, with `null` at each missing child. Write it as one string of comma-separated tokens by the preorder walk: a weight is written first, then its left hanging, then its right hanging, and every empty hanging, including those beneath leaves, is written as `#`.

**Constraints.** 1 <= values.length <= 3000 with the first entry not null, and weights are integers between 0 and 100000.

**Example 1.** Input `values = [1, 2, 3, null, null, 4, 5]`, output `"1,2,#,#,3,4,#,#,5,#,#"`.

**Example 2.** Input `values = [1, null, 2]`, output `"1,#,2,#,#"`.

**Hint.** How many tokens does a tree with n weights produce, and what does a leaf write after its own value?

**Changed decision.** Empty children are written out as markers, so every call writes either one marker or a weight with two sub-writes.

#### [Vary] Recursive Decoder (Author exercise)
<!-- id: tb-recursive-decoder -->

**Prerequisites.** The Preorder With Null Markers rung.

**Problem.** Given the comma-separated text produced by the marker-based preorder write, rebuild the tree and return it as a level-order array with trailing `null` entries removed. Each recursive call must consume exactly the tokens of one subtree, and the shared position must advance once per token.

**Constraints.** The text holds between 1 and 6001 tokens, every token is `#` or an integer between 0 and 100000, and the tokens form a complete tree.

**Example 1.** Input `text = "1,2,#,#,3,4,#,#,5,#,#"`, output `[1, 2, 3, null, null, 4, 5]`.

**Example 2.** Input `text = "1,#,2,#,#"`, output `[1, null, 2]`.

**Hint.** After the left call returns, where must the shared position stand for the right call to begin correctly?

**Changed decision.** The position is one shared counter that each call advances in place, so the left call tells the right call where to start without any return value.

#### [Boundary] Empty, Negative, And Multi-Digit Values (Author exercise)
<!-- id: tb-codec-edge-values -->

**Prerequisites.** The Recursive Decoder rung and the choice of a delimiter.

**Problem.** Encode a tree with the same marker-based preorder scheme when weights may be negative, may have many digits, and the tree may be empty, in which case the text is a single marker. Return the text, and make sure that decoding it yields the same tree.

**Constraints.** 0 <= values.length <= 2000 and weights are integers between -2147483648 and 2147483647.

**Example 1.** Input `values = []`, output `"#"`.

**Example 2.** Input `values = [-10, null, 2000000000]`, output `"-10,#,2000000000,#,#"`.

**Hint.** Which characters can appear inside a number token, and which character can be chosen to separate tokens without confusion?

**Changed decision.** A comma separates tokens and a lone `#` stands for emptiness, so the text of an empty tree is still a valid, non-empty card.

#### [Recognize] Serialize and Deserialize Binary Tree (LeetCode 297)
<!-- id: tb-serialize-binary-tree -->

**Prerequisites.** The Empty, Negative, And Multi-Digit Values rung and the queue discipline of level order.

**Problem.** Design a matched codec that writes a tree level by level: the encoder visits nodes in queue order, writes the weight of each present node or the word `null` for an absent child, and gives every present node exactly two child tokens. The decoder rebuilds the tree from the text with a queue and a moving index. Return the encoded text and whether decoding it gives back the original array.

**Constraints.** 0 <= values.length <= 5000 and weights are integers between -1000 and 1000.

**Example 1.** Input `values = [1, 2, 3, null, null, 4, 5]`, output `["1,2,3,null,null,4,5,null,null,null,null", true]`.

**Example 2.** Input `values = [1, null, 2]`, output `["1,null,2,null,null", true]`.

**Hint.** Which nodes are put into the queue, and how many tokens does each of them read back from the text?

**Changed decision.** The grammar is level order with a queue instead of preorder with recursion, so the decoder reads two tokens per dequeued node and needs no call stack.
