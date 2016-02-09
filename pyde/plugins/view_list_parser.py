from pyde.plugins.parser import SemanticNode, ParserRuleContext, SemanticRule,\
    Token, ContextSlice, Suggestion
    
class ViewListParser:
    def __init__(self):
        self.ast = {'view_name': ParserRuleContext(None)}
        self.semantic_ast = {'view_name': SemanticRule('view_name', self.ast['view_name'], {'value': {'name': 'value'}})}    

    def parse(self, text, text_range):
        self.tokens = [Token('VIEW_NAME', ContextSlice(text_range[0], text_range[1]), text)]
        self.parse_tree = ParserRuleContext(None)
        self.parse_tree.append(self.tokens[0])
        self.semantic_tree = SemanticNode(self.semantic_ast['view_name'], self.parse_tree)
        self.semantic_tree.value = text

        return self.semantic_tree
    
    def completion_suggestions(self, text, text_range):
        return [Suggestion(type='view_name', feature=('value', None), node=self.semantic_tree, parse_node=self.parse_tree)]
