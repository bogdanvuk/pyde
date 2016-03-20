import pyde.plugins.parser
from pyde.plugins.parser import Antlr4GenericParser 
# import json
# import subprocess
# from pyde.plugins.parser import ContextBuilder, Context,ParseTreeVisitor,\
#     ContextVisitor, ContextSlice, Token, NodeVisitor, get_ctx_parent_of_type
# import os
# import collections
# 
# def parse_tree_gen(grammar_file, grammar_text):
#         
#     p = subprocess.Popen(['java', 'pyinterface.Main', 
#                           'antlr4.antlr4', 
#                           'grammarSpec', '-json', '-file', grammar_file], stdout=subprocess.PIPE).communicate()[0]
#     parse_out = json.loads(p.decode())
#     tokens = pyde.plugins.parser.create_tokens(parse_out['tokens'], grammar_text, (0, len(grammar_text)))
#     dict_tree = parse_out['tree']
# #             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
#     parse_builder = pyde.plugins.parser.ParseTreeBuilder(tokens, (0, len(grammar_text)))
#     parse_tree = parse_builder.visit(dict_tree)
#     builder = ContextBuilder(tokens, {})
#     builder.visit(parse_tree)
#     
#     return builder.tree
# 
# def get_rules(parse_tree):
#     rules = {}
#     for rule in parse_tree['rules']['rule']:
#         name = grammar_text[rule['name'].slice.start:rule['name'].slice.stop]
#         ctx = Context()
#         ctx.type = name
#         if 'alt' in rule['ruleBlock'].features:
#             ctx['alt'] = rule['ruleBlock']['alt']
#             
#         rules[name] = ctx
#         if name == start_rule_name:
#             start_rule = ctx
#     
# #     for _, rule in rules.items():
# #         for alt in rule['alt']:
# #             for e in alt['elem']:
# #                 name = grammar_text[e.slice.start:e.slice.stop]
# #                 e['rule'] = rules[name]
#     return rules
# 
# # def visit_rule(node):
# #     for alt in node.rule['alt']:
# 
# # class GrammarParseVisitor(ParserRuleContextVisitor):
# #     def visit_id(self, node):
# #         pass
# 
# class LabeledElementSearch(NodeVisitor):
#     class FoundElement(Exception):
#         def __init__(self, ctx):
#             self.ctx = ctx
#     
#     def search(self, rule, lbl_id):
#         self.lbl_id = lbl_id
# 
#         try:
#             self.visit(rule)
#         except self.FoundElement as e:
#             return e.ctx
#         
#         return None
#         
#     def visit_labeledElement_id(self, node):
#         text = node.rule.text
#         if text[:-1] == self.lbl_id:
#             raise self.FoundElement(node)
# 
# class NextRulesVisitor_old:
#     def __init__(self, rules):
#         self.rules = rules
#         self.next_rules = []
# 
#     def list_alt_start_rules(self, alt):
#         for elem in alt['elem']:
#             finished = self.list_elem_start_rules(elem)
#             
#             if finished:
#                 return True
# 
#     def list_block_start_rules(self, block):
#         if 'alt' in block:
#             for alt in block['alt']:
#                 self.list_alt_start_rules(alt)
#         else:
#             self.next_rules.append(block)
# 
#     def list_elem_start_rules(self, elem):
#         if 'block' in elem:
#             block = elem['block']
#             self.list_block_start_rules(block['altList'])
#         elif 'name' in elem:
#             rule_ref = elem['name'].rule.text
#             child_rule = self.rules[rule_ref]
#             self.list_block_start_rules(child_rule)
#         elif 'lbl' in elem:
#             #Although 'labeledElement' rule is not identical to 'element'
#             #rule, it has 'name' and 'block' features which behave the
#             #same
#             self.list_elem_start_rules(elem['lbl'])
#               
#         # If next element is not optional, we are done searching for next
#         # rule in this side of tree
#         if ('sfx' not in elem) or (elem['sfx'].type == 'PLUS'):
#             return True
#         else:
#             return False
# 
#     def next_element_start_rules(self, elem):
#         while elem is not None:
#             path = elem.get_feature_in_parent()
#             alt = elem.parent
#         
#             # Can current element be repeated by * or + ? If so, the next rule can
#             # be the present rule repeated
#             if ('sfx' in elem) and (elem['sfx'].type in ['STAR', 'PLUS']):
#                 self.list_elem_start_rules(elem)
#             
#             # If current element is one in the sequence of elements in the parent
#             # alternative, the next rule is searched within th next element in the
#             # sequence.   
#             if path[1] + 1 < len(alt['elem']):
#                 next_elem = alt['elem'][path[1] + 1]
#                 if self.list_elem_start_rules(next_elem):
#                     return True
# 
#             elem = elem.get_parent_of_type('element')
#             
#         return False
#         
#     def get_element_rule_for_ctx(self, ctx):
#         path = ctx.get_feature_in_parent()
#         rule = self.rules[ctx.parent.type] #Get the rule associated with parent of ctx
#         
#         #Find the 'lblElement' that connects to the rule associated with ctx
#         v = LabeledElementSearch()
#         lbl = v.search(rule, path[0])
#         #Get the 'element' rule which is the parent of lbl
#         return lbl.get_parent_of_type('element')
# 
#     def get_next_rules(self, ctx):
#         finished = False
#         while (not finished) and (ctx.parent is not None):
#             elem_rule = self.get_element_rule_for_ctx(ctx)
#             finished = self.next_element_start_rules(elem_rule)
#             ctx = ctx.parent
#         
#         return self.next_rules
# 
# class ParserRuleContext(list):
#     def __init__(self, parent):
#         self.parent = parent
#         super().__init__()
# 
#     def root(self):
#         node = self
#         while (node.parent is not None):
#             node = node.parent
#         
#         return node
#     
#     def __repr__(self):
# #         return super(ParserRuleContext, self).__repr__()
#         if hasattr(self, 'type'):
#             text = self.type
#             if len(self) > 1:
# #                 print(super(ParserRuleContext, self).__repr__())
#                 text += ': ' + super(ParserRuleContext, self).__repr__()
#             return text
#         else:
#             return super(ParserRuleContext, self).__repr__()
#         
#     @property
#     def slice(self):
#         return ContextSlice(self[0].slice.start, self[-1].slice.stop)
# 
# class GrammarASTBuilder:
#     def __init__(self):
#         self.cur_parent = None 
#     
#     def visit(self, node):
#         rule = ParserRuleContext(self.cur_parent)
#         for k,v in node.items():
#             if k == 'feature':
#                 # remove '_' at the end of the feature name, the hack to allow
#                 # for features to have same names as rules in ANTLR4
#                 setattr(rule, k, v[:-1])  
#             elif k != 'children':
#                 setattr(rule, k, v)
#         
#         self.cur_parent = rule
#         for c in node['children']:
#             rule.append(self.visit(c))
#             
#         return rule
#     
# class SemanticNode:
#     def __init__(self, features, rule, parse_node = None, parent = None):
#         self.features = features
#         self.parse_node = parse_node
#         self.type = rule.type
#         self.rule = rule
#         self.parent = parent
# 
# class SemanticTreeBuilder(ParseTreeVisitor):
#     def __init__(self, semantic_ast, common_fields):
#         self.cur_parent = None
#         self.common_fields = common_fields
#         self.semantic_ast = semantic_ast
#         
#     def visit(self, node):
#         if hasattr(node, 'features') and node.features:
#             parent = self.cur_parent
#             semantic_node = self.semantic_ast[node.type](parse_node = node, parent=parent)
#             node.semantic_node = semantic_node
#             self.cur_parent = semantic_node 
#             for k,v in node.features.items():
#                 if isinstance(v, collections.Iterable):
#                     setattr(semantic_node, k, [])
#                     for n in v:
#                         getattr(semantic_node, k).append(self.visit(node[n]))
#                 else:
#                     setattr(semantic_node, k, self.visit(node[v]))
# 
#             for k,v in self.common_fields.items():
#                 setattr(semantic_node, k, v)
# 
#             self.cur_parent = parent
#             return semantic_node
#         else:
#             return node.text
#     
# class SemanticRule:
#     def __init__(self, type_name, rule):
#         self.type = type_name
#         self.rule = rule
#         self.features = {}
#         
#     def feature_for_state(self, state):
#         for n, f in self.features.items():
#             if s in f['states']:
#                 return n
#             
#         return None
#     
#     def __call__(self, **kwargs):
#         return SemanticNode(list(self.features.keys()), self, **kwargs)        
#     
# class SemanticASTBuilder(ParseTreeVisitor):
#     def __init__(self, ast):
#         self.ast = ast
#         
#     def build(self):
#         self.semantic_ast = {}
#         for name, rule in self.ast.items():
#             self.semantic_rule = SemanticRule(name, rule)
#             self.visit(rule)
#             self.semantic_ast[name] = self.semantic_rule
#         
#         return self.semantic_ast
#     
#     def visit(self, node):
#         if hasattr(node, 'feature'):
#             if node.feature not in self.semantic_rule.features:
#                 self.semantic_rule.features[node.feature] = {'name': node.feature, 'states': [], 'rules': []}
#             
#             self.semantic_rule.features[node.feature]['states'].append(node.state)
#             self.semantic_rule.features[node.feature]['cumul'] = node.featureAccumulation
#             self.semantic_rule.features[node.feature]['rules'].append(node)
#             
#         super().visit(node)
#         
# class ParseTreeBuilder:
#     def __init__(self, tokens, common_fields):
#         self.cur_parent = None 
#         self.common_fields = common_fields
#         self.tokens = tokens
#     
#     def visit(self, node):
#         if node['type'] == 'tokref':
#             if node['index'] >= 0:
#                 self.tokens[node['index']].parent = self.cur_parent
#                 return self.tokens[node['index']]
#             else:
#                 return None
#         else:
#             parent = self.cur_parent
#             rule = ParserRuleContext(parent)
#             self.cur_parent = rule
#             for k,v in node.items():
#                 if k != 'children':
#                     setattr(rule, k, v)
#                     
#             for k,v in self.common_fields.items():
#                 setattr(rule, k, v)
#             
#             for c in node['children']:
#                 rule.append(self.visit(c))
#             
#             self.cur_parent = parent
#             return rule
# 
# 
# class ASTStateVisitor(ParseTreeVisitor):
#     def __init__(self):
#         self.states = {}
#         
#     def visit(self, node):
#         if hasattr(node, 'state'):
#             if node.state >= 0:
#                 self.states[node.state] = node
#                 
#         return super().visit(node)
# 
# def createASTStatesMap(rules):
#     v = ASTStateVisitor()
#     for _, r in rules.items():
#         v.visit(r)
#         
#     return v.states
# 
# def getSuggestions(text):
#     loadGrammarAst('linpath')         
#     p = subprocess.Popen(['java', 'pyinterface.CompletionSuggestions', 
#                       'linpath', 'main', text], stdout=subprocess.PIPE).communicate()[0]
# 
#     suggestions = json.loads(p.decode())
#     return suggestions
# 
# class NextRulesVisitor(ParseTreeVisitor):
#     def __init__(self, rules):
#         self.rules = rules
#         self.next_rules = []
# 
#     def visit(self, node):
#         if hasattr(node, 'feature'):
#             self.next_rules.append(node)
#         return super().visit(node)
#     
#     def visit_ALT(self, node):
# #         if hasattr(node[0], 'feature'):
# #             self.next_rules.append(node[0])
#         for n in node: 
#             ret = self.visit(n)
#             if ret:
#                 return True
#             
#         return False
#     
#     def visit_SET(self, node):
#         for n in node:
#             self.visit(n)
#             
#         return True
#         
#     def visit_OPTIONAL(self, node):
#         self.visit(node[0])
#         return False
#     
#     def visit_CLOSURE(self, node):
#         self.visit(node[0])
#         return False
# 
#     def visit_POSITIVE_CLOSURE(self, node):
#         self.visit(node[0])
#         return False
#     
#     def visit_TOKEN_REF(self, node):
#         return True
#     
#     def visit_RULE_REF(self, node):
#         return self.visit(self.rules[node.ref])
#     
# #     def visit_BLOCK(self, node):
# #         pass
#         
# class RuleByPositionVisitor(ParseTreeVisitor):
# 
#     class FoundLeafException(Exception):
#         def __init__(self, node):
#             self.node = node
# 
#     def __init__(self, root):
#         self.root = root
#  
#     def context_at(self, pos):
#         self.context = None
#         self.pos = pos
#         try:
#             self.visit(self.root)
#         except self.FoundLeafException as e:
#             return e.node
#     
#     def visit(self, node):
#         if node.slice.contains(self.pos):
#             super().visit(node)
#             raise self.FoundLeafException(node)
#         
# 
# def start_of_carret_token(tokens, carret_index):
#     for t in parser.tokens:
#         if t.slice.start >= carret_index:
#             return carret_index
#         elif t.slice.stop > carret_index:
#             return t.slice.start
# 
# def create_tokens(token_json, text, active_range):
# #     active_range = editor.active_range()
#     tokens = []
#     for tj in token_json:
#         t = tj['type']
#         s = ContextSlice(tj['start'] + active_range[0], tj['stop'] + active_range[0] + 1)
#         tokens.append(Token(t,s,tj['text']))
# 
#     return tokens
# 
# class TokenSequence(list):
#     def __init__(self, tokens_js = None, pos_offset=0):
#         super().__init__()
#         for tj in tokens_js:
#             type_name = tj['type']
#             s = ContextSlice(tj['start'] + pos_offset, tj['stop'] + pos_offset + 1)
#             t = Token(type_name,s,tj['text'])
#             self.append(t)
#     
#     def token_at_pos(self, pos):
#         for i,t in enumerate(self):
#             if t.slice.start >= pos:
#                 return i,t
# 
# def buildSemanticAst(ast):
#     b = SemanticASTBuilder(ast)
#     return b.build()
# 
# class Antlr4GenericParser:
#     
#     def __init__(self, language, start_rule):
#         self.language = language
#         self.start_rule = start_rule
#         self.ast = loadGrammarAst('linpath')
#         self.semantic_ast = buildSemanticAst(self.ast)
# #         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'grammars'))
# #         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
#     
#     def parse(self, text, text_range):
#         active_text = text[text_range[0]: text_range[1]]
#         self.dirty = False
#         p = subprocess.Popen(['java', 'pyinterface.Main', 
#                               self.language + '.' + self.language, 
#                               self.start_rule, '-json', active_text], stdout=subprocess.PIPE).communicate()[0]
#         parse_out = json.loads(p.decode())
#         self.tokens = TokenSequence(parse_out['tokens'], text_range[0])
#         dict_tree = parse_out['tree']
# #             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
#         common_fields = {'ast': self.ast, 'token': self.tokens}
#         parse_builder = ParseTreeBuilder(self.tokens, common_fields)
#         self.parse_tree = parse_builder.visit(dict_tree)
#         
#         common_fields = {'ast': self.semantic_ast}
#         builder = SemanticTreeBuilder(self.semantic_ast, common_fields)
#         self.semantic_tree = builder.visit(self.parse_tree)
#         return self.semantic_tree
# 
# # def find(rule, states, state_stack):
# #     for s in state_stack:
# #    
# 
# def semantic_node_for_token(t):
#     rule_node = t
#     while(rule_node is not None):
#         if hasattr(rule_node, 'semantic_node'):
#             return rule_node.semantic_node
#         
#         rule_node = rule_node.parent
#         
#     return None


if __name__ == "__main__":
#     text = 'ddic.'
    text = 'x=1'
    carret_index = 2
#     parser = Antlr4GenericParser('python3', 'file_input')
#     parser = Antlr4GenericParser('linpath', 'main')
#     with open('/home/bvukobratovic/Downloads/and.vhd') as f:
#         text = f.read()
        
    parser = Antlr4GenericParser('vhdl', 'expression')
#     import time
#     start_time = time.time()
#     ret = parser.parser_io.communicate(text)
    tree = parser.parse(text, (0, len(text)))
#     print("--- %s seconds ---" % (time.time() - start_time))
    s = parser.completion_suggestions(text, (0, carret_index))
    for i in s: 
        print(i)
#     parser.parse(test_text, (0, len(test_text)))
# 
#     i, carret_token = parser.tokens.token_at_pos(carret_index)
#     if carret_index == carret_token.slice.start:
#         pre_carret_token = parser.tokens[i-1] 
# #     carret_token_start_index = start_of_carret_token(parser.tokens, carret_index)
#     
#     carret_ctx = semantic_node_for_token(carret_token)
#     pre_carret_ctx = semantic_node_for_token(pre_carret_token)
#     
# #         v = RuleByPositionVisitor(parser.parse_tree)
# #         cur_ctx = v.context_at(carret_token_start_index)
# #         prev_ctx = v.context_at(carret_token_start_index - 1)
#     
#     suggestions = getSuggestions(test_text[:carret_index])
#     suggest_rules = {}
#     for s in suggestions:
#         grammar = states[s['state_stack'][0]]
#         node = pre_carret_ctx
#         while(node != None):
#             for state in s['state_stack']:
#                 for n, f in node.rule.features.items():
#                     if state in f['states']:
#                         if f['cumul']:
#                             getattr(node, f).append()
#                         pass
# 
#             node = node.parent  
                    
#                 grammar = states[state]
#                 
#             if hasattr(grammar, 'feature'):
#                 suggest_rules[id(grammar)] = grammar
#             v = NextRulesVisitor(rules)
#             v.visit(grammar)
#             for rule in v.next_rules:
#                 suggest_rules[id(rule)] = rule
    
#     for _, rule in suggest_rules.items():
#         print('visit_' + rule.root().name + '_' + rule.feature)
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

    
