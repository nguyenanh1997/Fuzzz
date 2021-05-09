import re
import random
RE_NONTERMINAL= re.compile(r'(<[^>< ]*>)')
RE_NONTERMINAL1 = re.compile(r'(@[^@@ ]*@)')
def nonterminals(expansion, charLeft, charRight ):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(re.compile(r'('+charLeft+'[^'+charRight+charLeft+' ]*'+charRight+')'), expansion)

START_SYMBOL = "@start@"

def simple_grammar_fuzzer(grammar,  charLeft, charRight, start_symbol=START_SYMBOL,
                          max_nonterminals=20, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term,charLeft, charRight)) > 0:
        symbol_to_expand = random.choice(nonterminals(term,charLeft, charRight))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term, charLeft, charRight)) < max_nonterminals:
            term = new_term
            #if log:
            #    print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            #if expansion_trials >= max_expansion_trials:
            #    raise ExpansionError("Cannot expand " + repr(term))

    return term