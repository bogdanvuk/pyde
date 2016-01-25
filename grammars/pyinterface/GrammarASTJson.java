package pyinterface;

import org.antlr.v4.tool.Grammar;
import org.antlr.v4.tool.GrammarParserInterpreter.BailButConsumeErrorStrategy;
import org.antlr.v4.tool.ast.AltAST;
import org.antlr.v4.tool.ast.BlockAST;
import org.antlr.v4.tool.ast.GrammarAST;
import org.antlr.v4.tool.ast.GrammarASTVisitor;
import org.antlr.v4.tool.ast.GrammarRootAST;
import org.antlr.v4.tool.ast.NotAST;
import org.antlr.v4.tool.ast.OptionalBlockAST;
import org.antlr.v4.tool.ast.PlusBlockAST;
import org.antlr.v4.tool.ast.PredAST;
import org.antlr.v4.tool.ast.RangeAST;
import org.antlr.v4.tool.ast.RuleAST;
import org.antlr.v4.tool.ast.RuleRefAST;
import org.antlr.v4.tool.ast.SetAST;
import org.antlr.v4.tool.ast.StarBlockAST;
import org.antlr.v4.tool.ast.TerminalAST;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;
import java.util.Stack;

import org.antlr.runtime.tree.CommonTree;
import org.antlr.v4.parse.ANTLRParser;
import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.RecognitionException;

public class GrammarASTJson implements GrammarASTVisitor {
	JSONObject allRules;
	JSONObject rule;
	Stack<JSONArray> childrenStack;
	Stack<JSONObject> jsonStack;
	Grammar g;

	public static class GatherNextPossibleRules extends BailButConsumeErrorStrategy {
		@Override
		public void recover(Parser recognizer, RecognitionException e) {
			super.recover(recognizer, e);
		}
	}
	
	public GrammarASTJson (Grammar g) {
        this.g = g;
    }
	
	public JSONObject toJson() {
		allRules = new JSONObject();
//		Stack<JSONArray> childrenStack = new Stack<JSONArray>();
//		Stack<JSONObject> jsonStack = new Stack<JSONObject>();
//
//		this.jsonStack.push(new JSONObject());
//    	this.childrenStack.push(new JSONArray());
    	g.ast.visit(this);
    	return this.allRules;
	}

	public void visitAll(CommonTree commonTree) {
		if( commonTree.getChildren() != null) {
			for( Object c: commonTree.getChildren()) {
				((GrammarAST) c).visit(this);
			}
		}
	}
	
	@Override
	public Object visit(GrammarAST node) {
		this.visitAll(node);		
		return null;
	}

	@Override
	public Object visit(GrammarRootAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(RuleAST node) {

		rule = new JSONObject();
		try {
			allRules.put(node.getRuleName(), rule);
			rule.put("fields", new JSONObject());
			rule.put("name", node.getRuleName());
		} catch (JSONException e) {
			e.printStackTrace();
		}
		for(GrammarAST field: node.getNodesWithType(ANTLRParser.ID)){
			String fieldName = field.getText();
			try {
				JSONObject jsField;
				if (!rule.has(fieldName)) {
					jsField = new JSONObject();
					jsField.put("name", fieldName);
					jsField.put("atn_states", new JSONArray());
					rule.put(fieldName, jsField);
				} else {
					jsField = (JSONObject) rule.get(fieldName);
				}
				JSONArray jsAtnStates = (JSONArray) jsField.get("atn_states");
				jsAtnStates.put(((GrammarAST) field.parent.getChild(1)).atnState.stateNumber);
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}
		//this.visitAll(node.getFirstDescendantWithType(ANTLRParser.ALT));		
		return null;
	}

	@Override
	public Object visit(BlockAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(OptionalBlockAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(PlusBlockAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(StarBlockAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(AltAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(NotAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(PredAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(RangeAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(SetAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(RuleRefAST node) {
		this.visitAll(node);
		return null;
	}

	@Override
	public Object visit(TerminalAST node) {
		this.visitAll(node);
		return null;
	}
	
}
