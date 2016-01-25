import pyde.plugins.parser
import json
import subprocess
from pyde.plugins.parser import ContextBuilder, Context,ParserRuleContextVisitor,\
    Antlr4GenericParser, ContextVisitor, NodeVisitor, get_ctx_parent_of_type
import os

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

class NextRulesVisitor:
    def __init__(self, rules):
        self.rules = rules
        self.next_rules = []

    def list_alt_start_rules(self, alt):
        for elem in alt['elem']:
            finished = self.list_elem_start_rules(elem)
            
            if finished:
                return True

    def list_block_start_rules(self, block):
        if 'alt' in block:
            for alt in block['alt']:
                self.list_alt_start_rules(alt)
        else:
            self.next_rules.append(block)

    def list_elem_start_rules(self, elem):
        if 'block' in elem:
            block = elem['block']
            self.list_block_start_rules(block['altList'])
        elif 'name' in elem:
            rule_ref = elem['name'].rule.text
            child_rule = self.rules[rule_ref]
            self.list_block_start_rules(child_rule)
        elif 'lbl' in elem:
            #Although 'labeledElement' rule is not identical to 'element'
            #rule, it has 'name' and 'block' features which behave the
            #same
            self.list_elem_start_rules(elem['lbl'])
              
        # If next element is not optional, we are done searching for next
        # rule in this side of tree
        if ('sfx' not in elem) or (elem['sfx'].type == 'PLUS'):
            return True
        else:
            return False

    def next_element_start_rules(self, elem):
        while elem is not None:
            path = elem.get_feature_in_parent()
            alt = elem.parent
        
            # Can current element be repeated by * or + ? If so, the next rule can
            # be the present rule repeated
            if ('sfx' in elem) and (elem['sfx'].type in ['STAR', 'PLUS']):
                self.list_elem_start_rules(elem)
            
            # If current element is one in the sequence of elements in the parent
            # alternative, the next rule is searched within th next element in the
            # sequence.   
            if path[1] + 1 < len(alt['elem']):
                next_elem = alt['elem'][path[1] + 1]
                if self.list_elem_start_rules(next_elem):
                    return True

            elem = elem.get_parent_of_type('element')
            
        return False
        
    def get_element_rule_for_ctx(self, ctx):
        path = ctx.get_feature_in_parent()
        rule = self.rules[ctx.parent.type] #Get the rule associated with parent of ctx
        
        #Find the 'lblElement' that connects to the rule associated with ctx
        v = LabeledElementSearch()
        lbl = v.search(rule, path[0])
        #Get the 'element' rule which is the parent of lbl
        return lbl.get_parent_of_type('element')

    def get_next_rules(self, ctx):
        finished = False
        while (not finished) and (ctx.parent is not None):
            elem_rule = self.get_element_rule_for_ctx(ctx)
            finished = self.next_element_start_rules(elem_rule)
            ctx = ctx.parent
        
        return self.next_rules

class ParserRuleContext(list):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

    def root(self):
        node = self
        while (node.parent is not None):
            node = node.parent
        
        return node
    
    def __repr__(self):
#         return super(ParserRuleContext, self).__repr__()
        if hasattr(self, 'type'):
            str = self.type
            if len(self) > 1:
#                 print(super(ParserRuleContext, self).__repr__())
                str += ': ' + super(ParserRuleContext, self).__repr__()
            return str
        else:
            return super(ParserRuleContext, self).__repr__()

class ParseTreeBuilder:
    def __init__(self):
        self.cur_parent = None 
    
    def visit(self, node):
        rule = ParserRuleContext(self.cur_parent)
        for k,v in node.items():
            if k == 'feature':
                # remove '_' at the end of the feature name, the hack to allow
                # for features to have same names as rules in ANTLR4
                setattr(rule, k, v[:-1])  
            elif k != 'children':
                setattr(rule, k, v)
        
        self.cur_parent = rule
        for c in node['children']:
            rule.append(self.visit(c))
            
        return rule

def loadGrammarAst(grammar):
    import pyde
    
    with open(os.path.join(pyde.__path__[0], '..', 'grammars', grammar, grammar + 'AST.js')) as ast_file:    
        ast_js = json.load(ast_file)

    rules = {}    
    for name, rule in ast_js.items():
        b = ParseTreeBuilder()
        ruleCtx = b.visit(rule)
        rules[name] = ruleCtx
        
    return rules

class ASTStateVisitor(ParserRuleContextVisitor):
    def __init__(self):
        self.states = {}
        
    def visit(self, node):
        if hasattr(node, 'state'):
            if node.state >= 0:
                self.states[node.state] = node
                
        return super().visit(node)

def createASTStatesMap(rules):
    v = ASTStateVisitor()
    for _, r in rules.items():
        v.visit(r)
        
    return v.states

def getSuggestions(text):
    loadGrammarAst('linpath')         
    p = subprocess.Popen(['java', 'pyinterface.CompletionSuggestions', 
                      'linpath', 'main', text], stdout=subprocess.PIPE).communicate()[0]

    suggestions = json.loads(p.decode())
    return suggestions

if __name__ == "__main__":
    rules = loadGrammarAst('linpath')
    states = createASTStatesMap(rules)
    suggestions = getSuggestions('')
    for s in suggestions:
        for state in s['state_stack']:
            grammar = states[state]
            if hasattr(grammar, 'feature'):
                print('visit_' + grammar.root().name + '_' + grammar.feature)
            pass
#     grammar_file = '../linpath/linpath.g4'
#     start_rule_name = 'main'
#     with open(grammar_file, 'r') as g:
#         grammar_text=g.read()
# 
#     parse_tree = parse_tree_gen(grammar_file, grammar_text)
#     parse_rules = get_rules(parse_tree)
# 
# #     test_text = "ddic[' ']\n"
# #     
# #     p = subprocess.Popen(['java', 'pyinterface.Main', 
# #                       'python3.python3', 
# #                       'file_input', '-gui', "ddic[' ']\n"], stdout=subprocess.PIPE).communicate()[0]
# #     p = subprocess.Popen(['java', 'pyinterface.Main', 
# #                       'linpath.linpath', 
# #                       'main', '-gui', test_text + '\n'], stdout=subprocess.PIPE).communicate()[0]
#     test_text = "view/proba/"
# 
#     parser = Antlr4GenericParser('linpath', 'main')
#     test_tree = parser.parse(test_text, (0, len(test_text)))
#     v = ContextVisitor(test_tree)
#     ctx = v.context_at(10)
#     v = NextRulesVisitor(parse_rules)
#     next_rules = v.get_next_rules(ctx)
#     pass
#     
# #     v = GrammarParseVisitor()
# #     v.visit()
#     
# #     root = Context()
# #     root.rule = start_rule

    
