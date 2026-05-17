import sys
#try
class NFAState:
    def __init__(self):
        self.transitions = {}  # {char: [states]}
        self.epsilons = []  # [states]
        self.token_name = None
        self.priority = float('inf')


class Automata:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def create_literal_nfa(char):
    s = NFAState()
    e = NFAState()
    if char != "":
        s.transitions[char] = [e]
    else:
        s.epsilons.append(e)
    return Automata(s, e)


def create_char_class_nfa(chars):
    s = NFAState()
    e = NFAState()
    for c in chars:
        s.transitions[c] = [e]
    return Automata(s, e)


def concat_nfa(a1, a2):
    a1.end.epsilons.append(a2.start)
    return Automata(a1.start, a2.end)


def union_nfa(a1, a2):
    s = NFAState()
    e = NFAState()
    s.epsilons.extend([a1.start, a2.start])
    a1.end.epsilons.append(e)
    a2.end.epsilons.append(e)
    return Automata(s, e)


def star_nfa(a):
    s = NFAState()
    e = NFAState()
    s.epsilons.extend([a.start, e])
    a.end.epsilons.extend([a.start, e])
    return Automata(s, e)


def plus_nfa(a):
    s = NFAState()
    e = NFAState()
    s.epsilons.append(a.start)
    a.end.epsilons.extend([a.start, e])
    return Automata(s, e)


def optional_nfa(a):
    s = NFAState()
    e = NFAState()
    s.epsilons.extend([a.start, e])
    a.end.epsilons.append(e)
    return Automata(s, e)


class RegexParser:
    def __init__(self, pattern):
        self.p = pattern
        self.pos = 0

    def parse(self):
        return self.parse_union()

    def parse_union(self):
        node = self.parse_concat()
        while self.pos < len(self.p) and self.p[self.pos] == '|':
            self.pos += 1
            node = union_nfa(node, self.parse_concat())
        return node

    def parse_concat(self):
        node = self.parse_rep()
        while self.pos < len(self.p) and self.p[self.pos] not in '|)':
            node = concat_nfa(node, self.parse_rep())
        return node

    def parse_rep(self):
        node = self.parse_atom()
        while self.pos < len(self.p) and self.p[self.pos] in '*+?':
            op = self.p[self.pos]
            self.pos += 1
            if op == '*':
                node = star_nfa(node)
            elif op == '+':
                node = plus_nfa(node)
            elif op == '?':
                node = optional_nfa(node)
        return node

    def parse_atom(self):
        if self.pos >= len(self.p): return create_literal_nfa("")
        char = self.p[self.pos]
        if char == '(':
            self.pos += 1
            node = self.parse_union()
            if self.pos < len(self.p): self.pos += 1  # skip ')'
            return node
        elif char == '[':
            self.pos += 1
            chars = set()
            while self.pos < len(self.p) and self.p[self.pos] != ']':
                if self.pos + 2 < len(self.p) and self.p[self.pos + 1] == '-':
                    start, end = ord(self.p[self.pos]), ord(self.p[self.pos + 2])
                    for c in range(start, end + 1): chars.add(chr(c))
                    self.pos += 3
                else:
                    if self.p[self.pos] == '\\': self.pos += 1
                    chars.add(self.p[self.pos])
                    self.pos += 1
            self.pos += 1  # skip ']'
            return create_char_class_nfa(chars)
        elif char == '\\':
            self.pos += 1
            c = self.p[self.pos]
            self.pos += 1
            return create_literal_nfa(c)
        else:
            self.pos += 1
            return create_literal_nfa(char)


def get_epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for nxt in s.epsilons:
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return frozenset(closure)


def move(states, char):
    nxt = set()
    for s in states:
        if char in s.transitions:
            nxt.update(s.transitions[char])
    return nxt


def build_dfa(token_specs):
    combined_start = NFAState()
    for priority, (name, regex) in enumerate(token_specs):
        parser = RegexParser(regex)
        automata = parser.parse()
        automata.end.token_name = name
        automata.end.priority = priority
        combined_start.epsilons.append(automata.start)

    start_closure = get_epsilon_closure({combined_start})
    dfa_states = {start_closure: 0}
    dfa_transitions = {}
    unmarked = [start_closure]
    state_to_token = {}

    while unmarked:
        T = unmarked.pop(0)

        best_prio = float('inf')
        for nfa_s in T:
            if nfa_s.token_name and nfa_s.priority < best_prio:
                best_prio = nfa_s.priority
                state_to_token[T] = nfa_s.token_name

        possible_chars = set()
        for nfa_s in T:
            possible_chars.update(nfa_s.transitions.keys())

        for c in possible_chars:
            U = get_epsilon_closure(move(T, c))
            if not U: continue
            if U not in dfa_states:
                dfa_states[U] = len(dfa_states)
                unmarked.append(U)
            if T not in dfa_transitions: dfa_transitions[T] = {}
            dfa_transitions[T][c] = U

    return start_closure, dfa_transitions, state_to_token


def scan(text, dfa_start, dfa_trans, state_to_token):
    pos = 0
    line, col = 1, 1

    print(f"\n{'Lexeme':<15} {'Token':<15} {'Position'}")
    print("-" * 50)

    while pos < len(text):
        if text[pos].isspace():
            if text[pos] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            pos += 1
            continue

        current = dfa_start
        last_accepting_token = None
        last_accepting_pos = -1
        temp_pos = pos

        while temp_pos < len(text):
            char = text[temp_pos]
            if current in dfa_trans and char in dfa_trans[current]:
                current = dfa_trans[current][char]
                temp_pos += 1
                if current in state_to_token:
                    last_accepting_token = state_to_token[current]
                    last_accepting_pos = temp_pos
            else:
                break

        if last_accepting_token:
            lexeme = text[pos:last_accepting_pos]
            lexeme_display = f"'{lexeme}'"
            print(f"{lexeme_display:<15} {last_accepting_token:<15} Line {line}, col {col}")
            col += (last_accepting_pos - pos)
            pos = last_accepting_pos
        else:
            print(f"\nLexing Error: Unexpected character '{text[pos]}' at Line {line}, col {col}")
            return False

    print("\nLexing Completed Successfully.")
    return True

if __name__ == "__main__":
    token_specs = [
        ("KW_IF", "if"), ("KW_THEN", "then"), ("KW_ELSE", "else"),
        ("KW_WHILE", "while"), ("KW_FOR", "for"), ("KW_RETURN", "return"),
        ("KW_INT", "int"), ("KW_FLOAT", "float"),
        ("KW_BREAK", "break"),
        ("KW_CONTINUE", "continue"),
        ("ID", "[A-Za-z][A-Za-z0-9_]*"),
        ("NUM", "[0-9]+(\\.[0-9]+)?"),
        ("EQ", "=="), ("NEQ", "!="), ("LE", "<="), ("GE", ">="),
        ("ASSIGN", "="), ("OP_PLUS", "\\+"), ("OP_MINUS", "-"), ("MUL", "\\*"), ("DIV", "/"),
        ("GT", ">"), ("LT", "<"),
        ("LPAREN", "\\("), ("RPAREN", "\\)"), ("LBRACE", "\\{"), ("RBRACE", "\\}"),
        ("SEMI", ";"), ("COMMA", ","),
    ]
    print("Building Lexical Analyzer (Regex -> NFA -> DFA)...")
    try:
        start_state, transitions, token_map = build_dfa(token_specs)
        print("Analyzer Ready!\n")

        print("--- Lexical Analyzer Test ---")
        print("Enter the text to scan (or press Enter for project sample):")
        user_input = input("> ").strip()

        if not user_input:
            user_input = "if x > y then {x=y; z=x-1} else x=y+5"
            print(f"Using sample input: {user_input}")

        scan(user_input, start_state, transitions, token_map)

    except Exception as e:
        print(f"An error occurred: {e}")