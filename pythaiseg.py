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
        candidate_trie = self.exhaustive_matching(text)
        sequences = self.serialize(candidate_trie)
        # return sequences

        final_sequences = []
        for sequence in sequences:
            is_words = [self.trie.lookup(word) >= 2 for word in sequence]
            complete = len([b for b in is_words if not b]) == 0
            if complete:
                final_sequences.append(sequence)

        return final_sequences

    def exhaustive_matching(self, chars):

        results = {}
        working_chars = ''
        future_chars = chars

        for char in chars:
            working_chars += char
            future_chars = future_chars[1:]
            lookup_result = self.trie.lookup(working_chars)
            if lookup_result == 0:
                # This is not a word, move back
                results[working_chars] = self.exhaustive_matching(future_chars)
                break

            elif lookup_result == 1:
                # This is a part of words
                if len(future_chars) == 0:
                    # If it is the end of the string, simply add as a word
                    results[working_chars] = {}
                pass

            elif lookup_result == 2:
                # This is the end and not part of words, set word
                results[working_chars] = self.exhaustive_matching(future_chars)
                break

            elif lookup_result == 3:
                # This is the end but part of words, mark location and go on
                results[working_chars] = self.exhaustive_matching(future_chars)
                pass

        return results

    def serialize(self, trie):
        sequences = []
        if len(trie) > 0:
            for word, next_trie in trie.items():
                next_sequences = self.serialize(next_trie)
                if len(next_sequences) == 0:
                    sequences.append([word])
                else:
                    for next_sequence in next_sequences:
                        sequences.append([word] + next_sequence)
        else:
            sequences = trie

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
                    return 0

            # check the word ending
            if '|' in p:
                # this is a word
                if len(p) == 1:
                    # this is the end of the word and not for another word (2)
                    return 2
                else:
                    # can also be beginning of another word (1+2 = 3)
                    return 3
            else:
                # this maybe a beginning of words (1)
                return 1
