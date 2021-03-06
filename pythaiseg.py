TYPE_ROOT_NODE = -1
TYPE_UNKNOWN_WORD = 0
TYPE_WORD_BEGINNING = 1
TYPE_WORD_CONTINUE = 2
TYPE_WORD_END = 3


class WordSegmentation:
    def __init__(self, dict_path='data/dict.txt'):
        self.trie = self.WordTrie(dict_path)
        pass

    def segment(self, text):
        results = []
        sentences = text.split(' ')
        for sentence in sentences:
            results.append(self.segment_with_no_spaces(sentence))

        return results

    def segment_with_no_spaces(self, text):
        root_node = self.Node("", TYPE_ROOT_NODE)
        root_node.children = self.exhaustive_matching(text)

        sequences = self.serialize(root_node)

        scores = []
        for sequence in sequences:
            s = [node.type for node in sequence]
            avg = sum(s)/len(s)
            scores.append(avg)

        final_sequences = []
        sorted_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        for sorted_index in sorted_indexes:
            final_sequences.append(sequences[sorted_index])

        return final_sequences

    def exhaustive_matching(self, chars):
        nodes = {}
        working_chars = ''
        future_chars = chars

        for char in chars:
            working_chars += char

            future_chars = future_chars[1:]
            lookup_result = self.trie.lookup(working_chars)

            if lookup_result == TYPE_UNKNOWN_WORD:
                # This is not a word, move back if not the beginning or just add this char
                if len(working_chars) != 1:
                    future_chars = char + future_chars
                    working_chars = working_chars[0:-1]
                if len(working_chars) > 0:
                    node = self.Node(working_chars, self.trie.lookup(working_chars))
                    nodes[working_chars] = node
                    node.children = self.exhaustive_matching(future_chars)
                break

            elif lookup_result == TYPE_WORD_BEGINNING:
                # This is a beginning of words
                if len(future_chars) == 0:
                    # If it is the end of the string, simply add as a word
                    node = self.Node(working_chars, lookup_result)
                    nodes[working_chars] = node
                pass

            elif lookup_result == TYPE_WORD_END:
                # This is the end and not part of words, set word
                node = self.Node(working_chars, lookup_result)
                nodes[working_chars] = node
                node.children = self.exhaustive_matching(future_chars)
                break

            elif lookup_result == TYPE_WORD_CONTINUE:
                # This is the end but part of words, mark location and go on
                node = self.Node(working_chars, lookup_result)
                nodes[working_chars] = node
                node.children = self.exhaustive_matching(future_chars)
                pass

        return nodes

    def serialize(self, node):
        # Create new sequences
        sequences = []
        if len(node.children) > 0:
            # If child nodes exist, perform sequence merging of each child nodes
            word_found = False
            for term, next_node in node.children.items():
                if next_node.is_word():
                    word_found = True

            for term, next_node in node.children.items():
                if word_found:
                    # If these children have at least one word, Ignore bad kids
                    if not next_node.is_word():
                        continue
                else:
                    # If this node is not a word, then try to merge to the next node
                    # if the merge becomes word, this means other branch got it, just ignore
                    if not node.is_word():
                        work_type = self.trie.lookup(node.term + term)
                        if work_type == TYPE_WORD_CONTINUE or work_type == TYPE_WORD_CONTINUE:
                            continue

                if len(next_node.children) > 0:
                    # If the child node also have children, go recursively extract it
                    child_sequences = self.serialize(next_node)
                    for child_sequence in child_sequences:
                        # Append each sequence to the array
                        sequences.append([next_node] + child_sequence)
                else:
                    # The child node is a leaf node, simply add to sequence
                    sequences.append([next_node])

        else:
            # If leaf node, just return it self, it must be an array for merging purpose
            sequences.append([self])

        return sequences

    @staticmethod
    def maximal_matching(sentences):
        output = []
        for sequences in sentences:
            token_counts = [len(sequence) for sequence in sequences]
            min_index = token_counts.index(min(token_counts))
            min_token_sentence = sequences[min_index]
            output.append(min_token_sentence)
        return output

    class Node:
        def __init__(self, term, type):
            self.term = term
            self.type = type
            self.children = {}

        def add_child(self, node):
            self.children[node.term] = node

        def is_word(self):
            return self.type == TYPE_WORD_END or self.type == TYPE_WORD_CONTINUE

    class WordTrie:
        def __init__(self, dict_path='data/dict.txt'):
            self.trie = {}
            self.build_trie(dict_path)

        def build_trie(self, dict_path):
            import codecs
            with codecs.open(dict_path, 'r', encoding='utf8') as f:
                for word in f:
                    self.add_word(word)

        def add_word(self, chars):
            chars = chars.strip()
            p = self.trie
            for char in chars:
                if char not in p:
                    # node never exist
                    p[char] = {}
                # move pointer to the next level
                p = p[char]
            # mark word ending
            p['|'] = True

        def lookup(self, chars):
            p = self.trie
            for char in chars:
                if char in p:
                    # move to the next level
                    p = p[char]
                else:
                    # this is not a word (0)
                    return TYPE_UNKNOWN_WORD

            # check the word ending
            if '|' in p:
                # this is a word
                if len(p) == 1:
                    # this is the end of the word and not for another word (3)
                    return TYPE_WORD_END
                else:
                    # can also be beginning of another word (2)
                    return TYPE_WORD_CONTINUE
            else:
                # this maybe a beginning of words (1)
                return TYPE_WORD_BEGINNING
