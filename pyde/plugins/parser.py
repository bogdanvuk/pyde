import grammars
import os
import subprocess
import collections
import json

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
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for c in node.features:
            child = node.features[c]
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


class ContextVisitor(NodeVisitor):

    class FoundLeafException(Exception):
        pass

    def __init__(self, root):
        self.root = root
 
    def context_at(self, pos):
        self.context = None
        self.pos = pos
        try:
            self.visit(self.root)
        except self.FoundLeafException:
            return self.context
    
    def visit(self, node):

        if node.slice.contains(self.pos):
            if not node.features:
                self.context = node
                raise self.FoundLeafException
            else:
                for c in node.features:
                    child = node.features[c]
                    if isinstance(child, list):
                        for i,elem in enumerate(child):
                            self.visit(elem)
                    else:
                        self.visit(child)

class ParserRuleContext(list):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        
    @property
    def slice(self):
        i_start = None
        for i,c in enumerate(self):
            start_slice = c.slice
            if start_slice is not None:
                i_start = i
                break
        else:
            return None

        for i, c in reversed(list(enumerate(self))):
            if i == i_start:
                end_slice = start_slice
                break
            else:
                end_slice = c.slice
                if end_slice is not None:
                    break
        else:
            return None
        
        return ContextSlice(start_slice.start, end_slice.stop)

class ParserRuleContextVisitor:
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

class Context:
    type = 'default'
    
    def __init__(self, parent=None):
        self.parent = parent
#         if parent is not None:
#             self.parent.features[name] = self
        self.features = {} #OrderedDict()
    
    def __str__(self):
        return uri2str(self.uri)
#         return '{0}: {1}-{2}: {3}'.format(self.name, self.start, self.stop, self.text)
    
    __repr__ = __str__
    
    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + list(self.get_feature_in_parent())
        else:
            uri = []
            
        return uri
    
    def get_parent_of_type(self, *args):
        ctx = self
        while ctx.parent is not None:
            if ctx.parent.type in args:
                return ctx.parent
        
            ctx = ctx.parent
            
        return None
    
    def get_first_child_of_type(self, *args):
        class ChildTypeVisitor(NodeVisitor):
            class FoundElement(Exception):
                def __init__(self, ctx):
                    self.ctx = ctx

            def __init__(self, node, *args):
                self.types = args
                try:
                    self.visit(node)
                except self.FoundElement as e:
                    return e.ctx
                
                return None
                
            def visit(self, node):
                if node.type in args:
                    raise self.FoundElement(node)
                
        return ChildTypeVisitor(self, *args)
    
    def get_feature_in_parent(self):
        return self.parent.get_feature_for_child(self)

    def get_feature_for_child(self, child):
        for name, feature in self.features.items():
            if isinstance(feature, list):
                for i, cl in enumerate(feature):
                    if cl == child:
                        return (name, i)
            else:
                if feature == child:
                    return (name,)
        return None

    
    def __iter__(self):
        return self.features.__iter__()
    
    def __getitem__(self, item):
        return self.features[item]

    def __setitem__(self, item, val):
        self.features[item] = val


class RuleContext(Context):
    type = 'parser_rule'

    @property
    def slice(self):
        return self.rule.slice

class ParseTreeBuilder:
    def __init__(self, tokens, active_range):
        self.cur_parent = None
        self.tree = None
        self.tokens = tokens
        self.cur_tok_index = -1
        self.active_range = active_range

    def visit(self, node):
        if node['type'] == 'tokref':
            return self.visit_token(node)
        else:
            return self.visit_rule(node)

    def visit_token(self, node):
        index = node['index']
        if index >= 0:
            self.cur_tok_index = index
            self.tokens[index].parent = self.cur_parent
            return self.tokens[index]
        else:
            t = node['toktype']
            if self.cur_tok_index >= 0: 
                start = self.tokens[self.cur_tok_index].slice.stop # + self.active_range[0]
            else:
                start = self.active_range[0]
                
            stop = self.tokens[self.cur_tok_index + 1].slice.start + 1 # + self.active_range[0]
            s = ContextSlice(start, stop)
            return Token(t,s)

    def visit_rule(self, node):
        #         context = Context(name=node['type'], parent=self.cur_parent)
        rule = ParserRuleContext(self.cur_parent)
        rule.type = node['type']
#         rule.editor = self.editor
        
        if self.tree is None:
            self.tree = rule
            
        self.cur_parent = rule
        
        if 'children' in node:        
            children = list(range(len(node['children'])))
        else:
            children = []
        
        for c in children:
            child = node['children'][c]
            rule.append(self.visit(child))
        
        rule.fields = {}
        for field_name in node['_fields']:
            rule.fields[field_name] = node[field_name] 

        self.cur_parent = rule.parent
            
        return rule

class ContextBuilder:

    def __init__(self, parse_tree, keywords):
        self.tree = None
        self.cur_parent = None
        self.parse_tree = parse_tree
        self.keywords = keywords

    def visit(self, node):
        if isinstance(node, Token):
            return self.visit_token(node)
        else:
            return self.visit_rule(node)

    def visit_token(self, token):
        context = RuleContext(self.cur_parent)
        context.type = token.type
        context.rule = token
        context.keywords = self.keywords
        return context

    def visit_rule(self, node):
        #         context = Context(name=node['type'], parent=self.cur_parent)
        context = RuleContext(self.cur_parent)
        context.type = node.type
        context.keywords = self.keywords
          
        if self.tree is None:
            self.tree = context

        self.cur_parent = context
        
        if node.fields:
            for field_name in node.fields:
                field = node.fields[field_name]
                if isinstance(field, int):
                    child = node[field]
                    context[field_name] = self.visit(child)
                elif isinstance(field, list):
                    field_val = []
                    for elem in field:
                        child = node[elem]
                        field_val.append(self.visit(child))
                        
                    context[field_name] = field_val
    
        self.cur_parent = context.parent
        context.rule = node
        
        if context.parent:
            if len(node) == 1:
                if not node.fields:
                    child = node[0]
                    return self.visit(child)
#                     free_children[0].parent = self.cur_parent
#                     return free_children[0]
#             elif len(children) > 1:
#                 if not node['_fields']:
#                     for n in free_children:
#                         context[n.name] = n
        
        context.rule.context = context
        return context

class Token:
    
    def __init__(self, t, s, text=''):
        self.type = t
        self.slice = s
        self.text = text
    
    def __repr__(self):
        return "{}: {}".format(self.type, self.slice.eval())
      
    def __str__(self):
        return self.text

def create_tokens(token_json, text, active_range):
#     active_range = editor.active_range()
    tokens = []
    for tj in token_json:
        t = tj['type']
        s = ContextSlice(tj['start'] + active_range[0], tj['stop'] + active_range[0] + 1)
        tokens.append(Token(t,s,text[s.start:s.stop]))

    return tokens

class Antlr4GenericParser:
    
    def __init__(self, language, start_rule):
        self.language = language
        self.start_rule = start_rule
#         grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'grammars'))
        grammars_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
        with open(os.path.join(grammars_path, language, language) + '.keywords') as data_file:    
            self.keywords = json.load(data_file)
    
    def parse(self, text, text_range):
        active_text = text[text_range[0]: text_range[1]]
        self.dirty = False
        p = subprocess.Popen(['java', 'pyinterface.Main', 
                              self.language + '.' + self.language, 
                              self.start_rule, '-json', active_text + '\n'], stdout=subprocess.PIPE).communicate()[0]
        parse_out = json.loads(p.decode())
        tokens = create_tokens(parse_out['tokens'], text, text_range)
        dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
        parse_builder = ParseTreeBuilder(tokens, text_range)
        parse_builder.visit(dict_tree)
        self.parse_tree = parse_builder.tree
        builder = ContextBuilder(tokens, self.keywords)
        builder.visit(self.parse_tree)
        self.tree = builder.tree
        return self.tree

        
def Antlr4ParserFactory(lang_name, start_rule):
    class Antlr4Parser(Antlr4GenericParser):
        def __init__(self):
            super().__init__(language=lang_name, start_rule=start_rule)
        
    return Antlr4Parser