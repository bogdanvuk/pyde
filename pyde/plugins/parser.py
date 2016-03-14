import grammars
import os
import subprocess
import collections
import json
from collections import namedtuple
from pyde.plugins.pipe_textio import PipeTextIO

uri_separator = '/'
os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

def get_ctx_parent_of_type(ctx, *args):
    while ctx.parent is not None:
        if ctx.parent.type in args:
            return ctx.parent
    
        ctx = ctx.parent
        
    return None

def parser_node_child_by_feature(node, feature):
    try:
        feature_index = node.features[feature[0]]
        
        if feature[1] is not None:
            feature_index = feature_index[feature[1]]
        
        return node[feature_index]
    except (KeyError, IndexError):
        pass
    
    return None

def semantic_for_state_stack(node, state_stack):
    for state in state_stack:
        for n, f in node.rule.features.items():
            if state in f['states']:
                if f['cumul']:
                    feature = (n, len(getattr(node, n)))
                else:
                    feature = (n, None)
                
                return node, feature

    return None, None

def semantic_feature_in_parent(node):
    if node.parent:
        for f in node.parent.features:
            if hasattr(node.parent, f):
                child = getattr(node.parent, f)
                if isinstance(child, list):
                    for i, elem in enumerate(child):
                        if elem == node:
                            return node.parent, (f, i)
                else:
                    if child == node:
                        return node.parent, (f, None)
    return None, None

def semantic_for_rule_node(rule_node):
    while((rule_node is not None) and (rule_node.parent is not None)):
        parent = rule_node.parent
        if hasattr(rule_node, 'semantic_node'):
            return rule_node, None
        elif hasattr(parent, 'features'):
            for f, child in parent.features.items():
                if isinstance(child, list):
                    for i, elem in enumerate(child):
                        if parent[elem] == rule_node:
                            return parent.semantic_node, (f, i)
                else:
                    if parent[child] == rule_node:
                        return parent.semantic_node, (f, None)
        
        rule_node = parent
        
    return None, None

class SequenceMatchError(Exception):
    pass

class NodeVisitor:

    def visit(self, node):
        """Visit a node."""
        if isinstance(node, SemanticNode):
            if node.type:
                method = 'visit_' + node.type
                visitor = getattr(self, method, self.generic_visit)
            else:
                visitor = self.generic_visit
    
            self.visit_all_enter(node)
            if node.parent is not None:
                method = 'visit_' + node.parent.type + '_' + self.cur_feature
                if hasattr(self, method):
                    getattr(self, method)(node)
    
            ret = visitor(node)
                    
            self.visit_all_exit(node)
            return ret
        else:
            return None
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for c in node.features:
            child = getattr(node, c, None)
            if child:
                self.cur_feature = c
                if isinstance(child, list):
                    for elem in child:
                        self.visit(elem)
                else:
                    self.visit(child)

class ContextSlice:
    def __init__(self, start, stop=None):
        if stop is None:
            stop = start
        
        self.stop = stop
        self.start = start
  
    def contains(self, subslice):
        if isinstance(subslice, int):
            subslice = ContextSlice(subslice)
            
        return (self.start <= subslice.start) and (self.stop > subslice.stop)


class ParseTreeVisitor:
    def visit(self, node):
        if node.type:
            method = 'visit_' + node.type
            visitor = getattr(self, method, self.generic_visit)
        else:
            visitor = self.generic_visit

        return visitor(node)
    
    def generic_visit(self, node):

        if isinstance(node, collections.Iterable):
            for n in node:
                self.visit(n)

def uri2str(self, separator = '/'):
    return separator + separator.join(map(str, self))

class Token:
    
    def __init__(self, t, s, text=''):
        self.type = t
        self.slice = s
        self.text = text
    
    def __repr__(self):
        return "{}: {}".format(self.type, self.text)
      
    def __str__(self):
        return self.text

class TokenSequence(list):
    def __init__(self, tokens_js = None, pos_offset=0):
        super().__init__()
        for tj in tokens_js:
            type_name = tj['type']
            s = ContextSlice(tj['start'] + pos_offset, tj['stop'] + pos_offset + 1)
            t = Token(type_name,s,tj['text'])
            t.index = len(self)
            self.append(t)
    
    def token_at_pos(self, pos):
        for t in self:
            if (pos > t.slice.start) and (pos <= t.slice.stop):
                return t
            
        return None

class GrammarASTBuilder:
    def __init__(self, state_rules = []):
        self.cur_parent = None
        self.state_rules = state_rules
    
    def visit(self, node):
        rule = ParserRuleContext(self.cur_parent)
        for k,v in node.items():
            if k == 'feature':
                # remove '_' at the end of the feature name, the hack to allow
                # for features to have same names as rules in ANTLR4
                setattr(rule, k, v[:-1])  
            elif k != 'children':
                setattr(rule, k, v)

        if rule.state >= 0:
            self.state_rules[rule.state] = rule
            
        self.cur_parent = rule
        for c in node['children']:
            rule.append(self.visit(c))
            
        return rule

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
            text = self.type
            if len(self) > 1:
                text += ': ' + super(ParserRuleContext, self).__repr__()
            return text
        else:
            return super(ParserRuleContext, self).__repr__()
        
    @property
    def slice(self):
        return ContextSlice(self[0].slice.start, self[-1].slice.stop)

class SemanticNode:
    def __init__(self, rule, parse_node = None, parent = None):
        self.features = list(rule.features.keys())
        self.parse_node = parse_node
        self.type = rule.type
        self.rule = rule
        self.parent = parent
        
    def __getitem__(self, feature):
        child = getattr(self, feature[0]);
        if feature[1]:
            return child[feature[1]]
        else:
            return child

class SemanticTreeBuilder(ParseTreeVisitor):
    def __init__(self, semantic_ast, common_fields):
        self.cur_parent = None
        self.common_fields = common_fields
        self.semantic_ast = semantic_ast
        
    def visit(self, node):
        if hasattr(node, 'features') and node.features:
            if node.type == 'use_clause':
                pass
            parent = self.cur_parent
            semantic_node = self.semantic_ast[node.type](parse_node = node, parent=parent)
            node.semantic_node = semantic_node
            self.cur_parent = semantic_node 
            for k,v in node.features.items():
                if isinstance(v, collections.Iterable):
                    setattr(semantic_node, k, [])
                    for n in v:
                        getattr(semantic_node, k).append(self.visit(node[n]))
                else:
                    setattr(semantic_node, k, self.visit(node[v]))

            for k,v in self.common_fields.items():
                setattr(semantic_node, k, v)

            self.cur_parent = parent
            return semantic_node
        elif (isinstance(node, collections.Iterable)) and (len(node) == 1):
            return self.visit(node[0])
        elif hasattr(node, 'text'):
            return node.text
        else:
            return ''

class SemanticRule:
    def __init__(self, type_name, rule, features=None):
        self.type = type_name
        self.rule = rule
        if features is None:
            features = {}
            
        self.features = features
        
    def feature_for_state(self, state):
        for n, f in self.features.items():
            if state in f['states']:
                return n
            
        return None
    
    def __call__(self, **kwargs):
        return SemanticNode(self, **kwargs)        

class SemanticASTBuilder(ParseTreeVisitor):
    def __init__(self, ast):
        self.ast = ast
        
    def build(self):
        self.semantic_ast = {}
        for name, rule in self.ast.items():
            self.semantic_rule = SemanticRule(name, rule)
            self.visit(rule)
            self.semantic_ast[name] = self.semantic_rule
        
        return self.semantic_ast
    
    def visit(self, node):
        if hasattr(node, 'feature'):
            if node.feature not in self.semantic_rule.features:
                self.semantic_rule.features[node.feature] = {'name': node.feature, 'states': [], 'rules': []}
            
            self.semantic_rule.features[node.feature]['states'].append(node.state)
            self.semantic_rule.features[node.feature]['cumul'] = node.featureAccumulation
            self.semantic_rule.features[node.feature]['rules'].append(node)
            
        super().visit(node)

class ParseTreeBuilder:
    def __init__(self, tokens, common_fields):
        self.cur_parent = None 
        self.common_fields = common_fields
        self.tokens = tokens
    
    def visit(self, node):
        if node['type'] == 'tokref':
            if node['index'] >= 0:
                self.tokens[node['index']].parent = self.cur_parent
                return self.tokens[node['index']]
            else:
                return None
        else:
            parent = self.cur_parent
            rule = ParserRuleContext(parent)
            self.cur_parent = rule
            for k,v in node.items():
                if k != 'children':
                    setattr(rule, k, v)
                    
            for k,v in self.common_fields.items():
                setattr(rule, k, v)
            
            for c in node['children']:
                rule.append(self.visit(c))
            
            self.cur_parent = parent
            return rule

Suggestion = namedtuple('Suggestion', 'type feature node parse_node')

class NextRulesVisitor(ParseTreeVisitor):
    def __init__(self, rules, semantic_node):
        self.rules = rules
        self.next_rules = []
        self.rule_name_stack = []
        self.semantic_node = semantic_node
        if self.semantic_node:
            self.parse_node = self.semantic_node.parse_node
        else:
            self.parse_node = None
 
    def visit(self, node):
        if hasattr(node, 'feature'):
            if node.featureAccumulation:
                feature = (node.feature, 0)
            else:
                feature = (node.feature, None)
            self.next_rules.append(Suggestion(type=node.root().name, feature=feature, node=self.semantic_node, parse_node=self.parse_node))
        return super().visit(node)
     
    def visit_ALT(self, node):
#         if hasattr(node[0], 'feature'):
#             self.next_rules.append(node[0])
        for n in node: 
            ret = self.visit(n)
            if ret:
                return True
             
        return False
     
    def visit_SET(self, node):
        for n in node:
            self.visit(n)
             
        return True
         
    def visit_OPTIONAL(self, node):
        self.visit(node[0])
        return False
     
    def visit_CLOSURE(self, node):
        self.visit(node[0])
        return False
 
    def visit_POSITIVE_CLOSURE(self, node):
        self.visit(node[0])
        return False
     
    def visit_TOKEN_REF(self, node):
        return True
     
    def visit_RULE_REF(self, node):
        if node.ref == 'expr':
            pass
        
        if node.ref in self.rule_name_stack:
            return True
        else:
            self.next_rules.append(Suggestion(type=node.ref, feature=None, node=self.semantic_node, parse_node=self.parse_node))
            self.rule_name_stack.append(node.ref)
            return self.visit(self.rules[node.ref])
#             self.rule_name_stack.pop()
#             return ret

class Antlr4GenericParser:
    
    def __init__(self, language, start_rule):
        self.language = language
        self.start_rule = start_rule
        self.ast = self.loadGrammarAst()
        self.semantic_ast = self.buildSemanticAst()
        self.parser_io = PipeTextIO('java', ['pyinterface.ParserIntf', self.language + '.' + self.language, self.start_rule])
        self.parser_io.connect()
        self.suggestion_io = PipeTextIO('java', ['pyinterface.CompletionSuggestions', self.language, self.start_rule])
        self.suggestion_io.connect()

#         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'grammars'))
#         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..'))

    def loadGrammarAst(self):
        import pyde
        
        with open(os.path.join(pyde.__path__[0], '..', 'grammars', self.language, self.language + 'AST.js')) as ast_file:    
            ast_js = json.load(ast_file)
    
        rules = {}
        self.state_ast_rules = {}  
        for name, rule in ast_js.items():
            b = GrammarASTBuilder(self.state_ast_rules)
            ruleCtx = b.visit(rule)
            rules[name] = ruleCtx
            
        return rules

    def buildSemanticAst(self):
        b = SemanticASTBuilder(self.ast)
        return b.build()
    
    def parse(self, text, text_range):
        active_text = text[text_range[0]: text_range[1]]
        self.dirty = False
        
#         p = subprocess.Popen(['java', 'pyinterface.Main', 
#                               self.language + '.' + self.language, 
#                               self.start_rule, '-json', active_text], stdout=subprocess.PIPE).communicate()[0]
#         parse_out = json.loads(p.decode())
#         if self.language == 'vhdl':
#             parser = Antlr4GenericParser('vhdl', 'design_file')
#             import time
#             start_time = time.time()
#             ret = parser.parser_io.communicate(active_text)
#         #     tree = parser.parse(text, (0, len(text)))
#             print("--- %s seconds ---" % (time.time() - start_time))
#             pass
        ret = self.parser_io.communicate(active_text)
        
#         if self.language == 'vhdl':
#             pass

        parse_out = json.loads(ret)
        self.tokens = TokenSequence(parse_out['tokens'], text_range[0])
        dict_tree = parse_out['tree']

        common_fields = {'ast': self.ast, 'token': self.tokens}
        parse_builder = ParseTreeBuilder(self.tokens, common_fields)
        self.parse_tree = parse_builder.visit(dict_tree)
        
        common_fields = {'ast': self.semantic_ast}
        builder = SemanticTreeBuilder(self.semantic_ast, common_fields)
        self.semantic_tree = builder.visit(self.parse_tree)
        return self.semantic_tree


    def place_suggestion(self, suggestion, node, feature):
#        if suggestion['type'] == 'org.antlr.v4.runtime.NoViableAltException':
        suggestions = []
        
        if suggestion['type'] == 'org.antlr.v4.runtime.NoViableAltException':
            v = NextRulesVisitor(self.ast, node)
            v.visit(self.state_ast_rules[suggestion['state_stack'][0]])
            return v.next_rules
        elif node is not None:
            node, feature = semantic_for_state_stack(node, suggestion['state_stack'])
            while (node):
                parse_node_child = parser_node_child_by_feature(node.parse_node, feature)
                suggestions.append(Suggestion(type=node.type, feature=feature, node=node, parse_node=parse_node_child))
                node, feature = semantic_feature_in_parent(node)
                                
        return suggestions
    
    def completion_suggestions(self, text, text_range):
        suggestions = []
        carret_index = text_range[1]
        carret_token = self.tokens.token_at_pos(carret_index)
#         if (carret_token is None) or (carret_index == carret_token.slice.start):
#             carret_token = self.tokens[carret_token.index-1] 
        if (carret_token is None):
            carret_token = self.tokens[0] 

        if not hasattr(carret_token, 'island_grammar_root'): 

            active_text = text[text_range[0]: carret_index]#carret_token.slice.start]
    #         p = subprocess.Popen(['java', 'pyinterface.CompletionSuggestions', 
    #                           self.language, self.start_rule, active_text], stdout=subprocess.PIPE).communicate()[0]
            ret = self.suggestion_io.communicate(active_text)
    #         ret = '[{"state_stack":[153],"type":"org.antlr.v4.runtime.NoViableAltException","token":0}]'
            suggestions_js = json.loads(ret)
            #     carret_token_start_index = start_of_carret_token(parser.tokens, carret_index)
            carret_ctx, feature = semantic_for_rule_node(carret_token)
            node = carret_ctx
            while (node):
                parse_node_child = parser_node_child_by_feature(node.parse_node, feature)
                suggestions.append(Suggestion(type=node.type, feature=feature, node=node, parse_node = parse_node_child))
                node, feature = semantic_feature_in_parent(node)

#             if (carret_ctx is not None): 
#                 suggestions.append(Suggestion(type=carret_ctx.type, feature=feature, node=carret_ctx))
        #        pre_carret_ctx = self.semantic_node_for_token(pre_carret_token)
                
            
            for s in suggestions_js:
                suggestions.extend(self.place_suggestion(s, carret_ctx, feature))
        
#         suggestions = []
#         if not suggestions_js:
#             v = NextRulesVisitor(self.ast)
#             v.visit(self.ast[self.start_rule])
#             suggestions.extend(v.next_rules)
#         else:
#             for s in suggestions_js:
#                 suggestions.extend(self.place_suggestion(s, carret_ctx))
#         
#         for s in suggestions: 
#             print(s)
        
        return suggestions
        
def Antlr4ParserFactory(lang_name, start_rule):
    class Antlr4Parser(Antlr4GenericParser):
        def __init__(self):
            super().__init__(language=lang_name, start_rule=start_rule)
        
    return Antlr4Parser