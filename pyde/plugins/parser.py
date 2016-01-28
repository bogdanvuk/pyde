import grammars
import os
import subprocess
import collections
import json
from collections import namedtuple

uri_separator = '/'
os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

def get_ctx_parent_of_type(ctx, *args):
    while ctx.parent is not None:
        if ctx.parent.type in args:
            return ctx.parent
    
        ctx = ctx.parent
        
    return None


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
            if t.slice.start >= pos:
                return t
            
        return None

class GrammarASTBuilder:
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
#                 print(super(ParserRuleContext, self).__repr__())
                text += ': ' + super(ParserRuleContext, self).__repr__()
            return text
        else:
            return super(ParserRuleContext, self).__repr__()
        
    @property
    def slice(self):
        return ContextSlice(self[0].slice.start, self[-1].slice.stop)

class SemanticNode:
    def __init__(self, features, rule, parse_node = None, parent = None):
        self.features = features
        self.parse_node = parse_node
        self.type = rule.type
        self.rule = rule
        self.parent = parent

class SemanticTreeBuilder(ParseTreeVisitor):
    def __init__(self, semantic_ast, common_fields):
        self.cur_parent = None
        self.common_fields = common_fields
        self.semantic_ast = semantic_ast
        
    def visit(self, node):
        if hasattr(node, 'features') and node.features:
            if 'callable' in node.features:
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
        elif (isinstance(node, collections.Iterable)) and (len(node) > 0):
            return self.visit(node[0])
        else:
            return node.text

class SemanticRule:
    def __init__(self, type_name, rule):
        self.type = type_name
        self.rule = rule
        self.features = {}
        
    def feature_for_state(self, state):
        for n, f in self.features.items():
            if state in f['states']:
                return n
            
        return None
    
    def __call__(self, **kwargs):
        return SemanticNode(list(self.features.keys()), self, **kwargs)        

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

Suggestion = namedtuple('Suggestion', 'type feature node')

class NextRulesVisitor(ParseTreeVisitor):
    def __init__(self, rules):
        self.rules = rules
        self.next_rules = []
        self.rule_name_stack = []
 
    def visit(self, node):
        if hasattr(node, 'feature'):
            self.next_rules.append(Suggestion(type=node.root().name, feature=node.feature, node=None))
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
            self.next_rules.append(Suggestion(type=node.ref, feature=None, node=None))
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
        pass
#         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'grammars'))
#         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..'))

    def loadGrammarAst(self):
        import pyde
        
        with open(os.path.join(pyde.__path__[0], '..', 'grammars', self.language, self.language + 'AST.js')) as ast_file:    
            ast_js = json.load(ast_file)
    
        rules = {}    
        for name, rule in ast_js.items():
            b = GrammarASTBuilder()
            ruleCtx = b.visit(rule)
            rules[name] = ruleCtx
            
        return rules

    def buildSemanticAst(self):
        b = SemanticASTBuilder(self.ast)
        return b.build()
    
    def parse(self, text, text_range):
        active_text = text[text_range[0]: text_range[1]]
        self.dirty = False
        p = subprocess.Popen(['java', 'pyinterface.Main', 
                              self.language + '.' + self.language, 
                              self.start_rule, '-json', active_text], stdout=subprocess.PIPE).communicate()[0]
        parse_out = json.loads(p.decode())
        self.tokens = TokenSequence(parse_out['tokens'], text_range[0])
        dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
        common_fields = {'ast': self.ast, 'token': self.tokens}
        parse_builder = ParseTreeBuilder(self.tokens, common_fields)
        self.parse_tree = parse_builder.visit(dict_tree)
        
        common_fields = {'ast': self.semantic_ast}
        builder = SemanticTreeBuilder(self.semantic_ast, common_fields)
        self.semantic_tree = builder.visit(self.parse_tree)
        return self.semantic_tree

    def semantic_node_for_token(self, t):
        rule_node = t
        while(rule_node is not None):
            if hasattr(rule_node, 'semantic_node'):
                return rule_node.semantic_node
            
            rule_node = rule_node.parent
            
        return None

    def place_suggestion(self, suggestion, node):
#        if suggestion['type'] == 'org.antlr.v4.runtime.NoViableAltException':
        suggestions = []
        while(node != None):
            for state in suggestion['state_stack']:
                for n, f in node.rule.features.items():
                    if state in f['states']:
                        suggestions.append(Suggestion(type=node.type, feature=n, node=node))
                        return suggestions
                    
        return suggestions
    
    def completion_suggestions(self, text, text_range):
        active_text = text[text_range[0]: text_range[1]]
        p = subprocess.Popen(['java', 'pyinterface.CompletionSuggestions', 
                          self.language, self.start_rule, active_text], stdout=subprocess.PIPE).communicate()[0]
    
        suggestions_js = json.loads(p.decode())
        carret_index = text_range[1]
        carret_token = self.tokens.token_at_pos(carret_index)
        if (carret_token is None) or (carret_index == carret_token.slice.start):
            pre_carret_token = self.tokens[carret_token.index-1] 
    #     carret_token_start_index = start_of_carret_token(parser.tokens, carret_index)
        
        carret_ctx = self.semantic_node_for_token(carret_token)
        pre_carret_ctx = self.semantic_node_for_token(pre_carret_token)
        
        suggestions = []
        if not suggestions_js:
            v = NextRulesVisitor(self.ast)
            v.visit(self.ast[self.start_rule])
            suggestions.extend(v.next_rules)
        else:
            for s in suggestions_js:
                suggestions.extend(self.place_suggestion(s, pre_carret_ctx))
        
        for s in suggestions: 
            print(s)
        
        return suggestions
        
def Antlr4ParserFactory(lang_name, start_rule):
    class Antlr4Parser(Antlr4GenericParser):
        def __init__(self):
            super().__init__(language=lang_name, start_rule=start_rule)
        
    return Antlr4Parser