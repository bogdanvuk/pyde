import pyde.plugins.parser
import json
import subprocess
from pyde.plugins.parser import ContextBuilder, Context,ParserRuleContextVisitor

class GrammarParseVisitor(ParserRuleContextVisitor):
    def visit_ruleref(self, node):
        pass

def parse_tree_gen(grammar_file, grammar_text):
        
    p = subprocess.Popen(['java', 'pyinterface.Main', 
                          'antlr4.antlr4', 
                          'grammarSpec', '-json', '-file', grammar_file], stdout=subprocess.PIPE).communicate()[0]
    parse_out = json.loads(p.decode())
    tokens = pyde.plugins.parser.create_tokens(parse_out['tokens'], (0, len(grammar_text)))
    dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
    parse_builder = pyde.plugins.parser.ParseTreeBuilder(tokens, (0, len(grammar_text)))
    parse_tree = parse_builder.visit(dict_tree)
    v = GrammarParseVisitor()
    v.visit(parse_tree)
    builder = ContextBuilder(tokens, {})
    builder.visit(parse_tree)

    return builder.tree

# def visit_rule(node):
#     for alt in node.rule['alt']:

if __name__ == "__main__":
    
    grammar_file = '../linpath/linpath.g4'
    start_rule_name = 'main'
    with open(grammar_file, 'r') as g:
        grammar_text=g.read()

    tree = parse_tree_gen(grammar_file, grammar_text)
    
#     v = GrammarParseVisitor()
#     v.visit()
    
    rules = {}
    for rule in tree['rules']['rule']:
        name = grammar_text[rule['name'].slice.start:rule['name'].slice.stop]
        ctx = Context()
        ctx.type = name
        if 'alt' in rule['ruleBlock'].features:
            ctx['alt'] = rule['ruleBlock']['alt']
            
        rules[name] = ctx
        if name == start_rule_name:
            start_rule = ctx
    
    for _, rule in rules.items():
        for alt in rule['alt']:
            for e in alt['elem']:
                name = grammar_text[e.slice.start:e.slice.stop]
                e['rule'] = rules[name]

#     root = Context()
#     root.rule = start_rule
    
    
    pass
