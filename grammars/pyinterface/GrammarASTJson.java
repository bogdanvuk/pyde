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

//		this.jsonStack.push(new JSONObject());
//    	this.childrenStack.push(new JSONArray());
    	g.ast.visit(this);
    	return this.allRules;
	}

	public JSONObject visitAll(GrammarAST node) {
		
		if (jsonStack != null) {
	   		jsonStack.push(new JSONObject());
	   		if (!childrenStack.isEmpty()) {
	   			childrenStack.peek().put(this.jsonStack.peek());
	   		}
	   		childrenStack.push(new JSONArray());
		}

		if( node.getChildren() != null) {
			for( Object c: node.getChildren()) {
				((GrammarAST) c).visit(this);
			}
		}
		
		if (jsonStack != null) {
			try {
				if (node.atnState == null) {
					jsonStack.peek().put("state", -1);
				} else {
					jsonStack.peek().put("state", node.atnState.stateNumber);
				}
				jsonStack.peek().put("type", ANTLRParser.tokenNames[node.getType()]);
				jsonStack.peek().put("children", childrenStack.pop());
			} catch (JSONException e) {
				e.printStackTrace();
			}
			return jsonStack.pop();
		}
		
		return null;
	}
	
	@Override
	public Object visit(GrammarAST node) {
		JSONObject rule;
		if (node.getType() == ANTLRParser.PLUS_ASSIGN || 
				node.getType() == ANTLRParser.ASSIGN) {
			rule = (JSONObject) ((GrammarAST) node.getChild(1)).visit(this);
			try {
				rule.put("feature", node.getChild(0).getText());
				if (node.getType() == ANTLRParser.PLUS_ASSIGN) {
					rule.put("featureAccumulation", true);
				} else {
					rule.put("featureAccumulation", false);
				}
			} catch (JSONException e) {
				e.printStackTrace();
			}
		} else { 
			rule = this.visitAll(node);
		}
		return rule;
	}

	@Override
	public Object visit(GrammarRootAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(RuleAST node) {

		
		childrenStack = new Stack<JSONArray>();
		jsonStack = new Stack<JSONObject>();
		
//		for(GrammarAST field: node.getNodesWithType(ANTLRParser.ID)){
//			String fieldName = field.getText();
//			try {
//				JSONObject jsField;
//				if (!rule.has(fieldName)) {
//					jsField = new JSONObject();
//					jsField.put("name", fieldName);
//					jsField.put("atn_states", new JSONArray());
//					rule.put(fieldName, jsField);
//				} else {
//					jsField = (JSONObject) rule.get(fieldName);
//				}
//				JSONArray jsAtnStates = (JSONArray) jsField.get("atn_states");
//				jsAtnStates.put(((GrammarAST) field.parent.getChild(1)).atnState.stateNumber);
//			} catch (JSONException e) {
//				e.printStackTrace();
//			}
//		}
		JSONObject rule = this.visitAll((GrammarAST) node.getFirstDescendantWithType(ANTLRParser.ALT));
		try {
			allRules.put(node.getRuleName(), rule);
			rule.put("fields", new JSONObject());
			rule.put("name", node.getRuleName());
		} catch (JSONException e) {
			e.printStackTrace();
		}
		childrenStack = null;
		jsonStack = null;
		return rule;
	}

	@Override
	public Object visit(BlockAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(OptionalBlockAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(PlusBlockAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(StarBlockAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(AltAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(NotAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(PredAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(RangeAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(SetAST node) {
		return this.visitAll(node);
	}

	@Override
	public Object visit(RuleRefAST node) {
		JSONObject rule = this.visitAll(node);
		try {
			rule.put("ref", node.getText());
		} catch (JSONException e) {
			e.printStackTrace();
		}

		return rule;
	}

	@Override
	public Object visit(TerminalAST node) {
		JSONObject rule = this.visitAll(node);
		try {
			rule.put("ref", node.getText());
		} catch (JSONException e) {
			e.printStackTrace();
		}

		return rule;
	}
	
}
