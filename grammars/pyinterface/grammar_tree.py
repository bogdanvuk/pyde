import pyde.plugins.parser
import json
import subprocess
from pyde.plugins.parser import ContextBuilder, Context,ParserRuleContextVisitor,\
    Antlr4GenericParser, ContextVisitor, NodeVisitor, get_ctx_parent_of_type

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

def list_alt_start_rules(alt, rules, start_rules):
    for elem in alt['elem']:
        finished = list_elem_start_rules(elem, rules, start_rules)
        
        if finished:
            return True

def list_block_start_rules(block, rules, start_rules):
    if 'alt' in block:
        for alt in block['alt']:
            list_alt_start_rules(alt, rules, start_rules)
    else:
        start_rules.append(block)

def list_elem_start_rules(elem, rules, start_rules):
    if 'block' in elem:
        block = elem['block']
        list_block_start_rules(block['altList'], rules, start_rules)
    elif 'name' in elem:
        rule_ref = elem['name'].rule.text
        child_rule = rules[rule_ref]
        list_block_start_rules(child_rule, rules, start_rules)
    elif 'lbl' in elem:
        rule_ref = elem['lbl']
        list_elem_start_rules(elem['lbl'], rules, start_rules)
          
    # If next element is not optional, we are done searching for next
    # rule in this side of tree
    if ('sfx' not in elem) or (elem['sfx'].type == 'PLUS'):
        return True
    else:
        return False

def next_element_start_rules(ctx, rules, next_rules):
    elem = ctx
    while True:
        elem = elem.get_parent_of_type('element')
        if elem is None:
            return False 
        
        path = elem.get_feature_in_parent()
        alt = elem.parent
    
        # Can current element be repeated by * or + ? If so, the next rule can
        # be the present rule repeated
        if ('sfx' in elem) and (elem['sfx'].type in ['STAR', 'PLUS']):
            list_elem_start_rules(elem, rules, next_rules)
        
        # If current element is one in the sequence of elements in the parent
        # alternative, the next rule is searched within th next element in the
        # sequence.   
        if path[1] + 1 < len(alt['elem']):
            next_elem = alt['elem'][path[1] + 1]
            if list_elem_start_rules(next_elem, rules, next_rules):
                return True
            
#             # If next element is not optional, we are done searching for next
#             # rule in this side of tree
#             if ('sfx' not in next_elem) or (next_elem['sfx'].type == 'PLUS'):
#                 return True
        
def next_rule_in_ctx(path, ctx, rules, next_rules):
    rule = rules[ctx.type]
    v = LabeledElementSearch()
    rule_ctx = v.search(rule, path[0])
#     altlist = get_ctx_parent_of_type(ctx, 'altlist', 'ruleAltList')
    
    return next_element_start_rules(rule_ctx, rules, next_rules)

def next_rule_in_parent(ctx, rules, next_rules):
    path = ctx.get_feature_in_parent()
    return next_rule_in_ctx(path, ctx.parent, rules, next_rules)
    
def next_rule(ctx, rules):
    next_rules = []
    finished = False
    while (not finished) and (ctx.parent is not None):
        finished = next_rule_in_parent(ctx, rules, next_rules)
        ctx = ctx.parent
    
    return next_rules

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
    ctx = v.context_at(9)
    next_rules = next_rule(ctx, parse_rules)
    pass
    
#     v = GrammarParseVisitor()
#     v.visit()
    
#     root = Context()
#     root.rule = start_rule

    
