import pyde.plugins.parser
import json
import subprocess
from pyde.plugins.parser import ContextBuilder, Context,ParserRuleContextVisitor,\
    Antlr4GenericParser, ContextVisitor, NodeVisitor

def parse_tree_gen(grammar_file, grammar_text):
        
    p = subprocess.Popen(['java', 'pyinterface.Main', 
                          'antlr4.antlr4', 
                          'grammarSpec', '-json', '-file', grammar_file], stdout=subprocess.PIPE).communicate()[0]
    parse_out = json.loads(p.decode())
    tokens = pyde.plugins.parser.create_tokens(parse_out['tokens'], grammar_text, (0, len(grammar_text)))
    dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
    parse_builder = pyde.plugins.parser.ParseTreeBuilder(tokens, (0, len(grammar_text)))
    parse_tree = parse_builder.visit(dict_tree)
    builder = ContextBuilder(tokens, {})
    builder.visit(parse_tree)
    
    return builder.tree

def get_rules(parse_tree):
    rules = {}
    for rule in parse_tree['rules']['rule']:
        name = grammar_text[rule['name'].slice.start:rule['name'].slice.stop]
        ctx = Context()
        ctx.type = name
        if 'alt' in rule['ruleBlock'].features:
            ctx['alt'] = rule['ruleBlock']['alt']
            
        rules[name] = ctx
        if name == start_rule_name:
            start_rule = ctx
    
#     for _, rule in rules.items():
#         for alt in rule['alt']:
#             for e in alt['elem']:
#                 name = grammar_text[e.slice.start:e.slice.stop]
#                 e['rule'] = rules[name]
    return rules

# def visit_rule(node):
#     for alt in node.rule['alt']:

# class GrammarParseVisitor(ParserRuleContextVisitor):
#     def visit_id(self, node):
#         pass

class LabeledElementSearch(NodeVisitor):
    class FoundElement(Exception):
        def __init__(self, ctx):
            self.ctx = ctx
    
    def search(self, rule, lbl_id):
        self.lbl_id = lbl_id

        try:
            self.visit(rule)
        except self.FoundElement as e:
            return e.ctx
        
        return None
        
    def visit_labeledElement_id(self, node):
        text = node.rule.text
        if text[:-1] == self.lbl_id:
            raise self.FoundElement(node)
    
def next_rule_in_ctx(path, ctx, rules):
    rule = rules[ctx.type]
    v = LabeledElementSearch()
    ctx = v.search(rule, path[0])
    pass

def next_rule_in_parent(ctx, rules):
    path = ctx.get_feature_in_parent()
    next_rule_in_ctx(path, ctx.parent, rules)
    pass
    
def next_rule(ctx, rules):
    next_rule_in_parent(ctx, rules)

if __name__ == "__main__":
    
    grammar_file = '../linpath/linpath.g4'
    start_rule_name = 'main'
    with open(grammar_file, 'r') as g:
        grammar_text=g.read()

    parse_tree = parse_tree_gen(grammar_file, grammar_text)
    parse_rules = get_rules(parse_tree)

#     test_text = "ddic[' ']\n"
#     
#     p = subprocess.Popen(['java', 'pyinterface.Main', 
#                       'python3.python3', 
#                       'file_input', '-gui', "ddic[' ']\n"], stdout=subprocess.PIPE).communicate()[0]
#     p = subprocess.Popen(['java', 'pyinterface.Main', 
#                       'linpath.linpath', 
#                       'main', '-gui', test_text + '\n'], stdout=subprocess.PIPE).communicate()[0]
    test_text = "view/proba/"

    parser = Antlr4GenericParser('linpath', 'main')
    test_tree = parser.parse(test_text, (0, len(test_text)))
    v = ContextVisitor(test_tree)
    ctx = v.context_at(10)
    next_rule(ctx, parse_rules)
    pass
    
#     v = GrammarParseVisitor()
#     v.visit()
    
#     root = Context()
#     root.rule = start_rule

    
