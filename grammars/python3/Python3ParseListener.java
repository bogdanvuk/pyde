package python3;

import java.io.StringWriter;
import java.lang.reflect.Field;
import java.util.Stack;

import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;

public class Python3ParseListener extends Python3BaseListener {
	Python3Parser parser;
	JSONObject jsonTop;
	Stack<JSONArray> childrenStack = new Stack<JSONArray>();
	Stack<JSONObject> jsonStack = new Stack<JSONObject>();
	
	public Python3ParseListener(Python3Parser parser, JSONObject json) {
        this.parser = parser;
        this.jsonStack.push(json);
    }
	
    public void enterEveryRule(ParserRuleContext ctx) {
//    	System.out.print(ctx.toString(this.parser));
//    	System.out.print(" ");
//    	System.out.println(ctx.toInfoString(parser));

    	if (!childrenStack.isEmpty()) {
    		this.jsonStack.push(new JSONObject());
    		childrenStack.peek().put(this.jsonStack.peek());
    	}
    	
    	try {
			jsonStack.peek().put("ctype", parser.getRuleNames()[ctx.getRuleIndex()]);
	    	childrenStack.push(new JSONArray());
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
   	
//    	System.out.print(ctx.getRuleContext().getRuleIndex());
//    	System.out.print(" : ");
//    	System.out.print(ctx.getText());
//    	System.out.print("\n");
    }
    
    public void exitEveryRule(ParserRuleContext ctx) {
    	try {
//    		jsonStack.peek().put("_fields", ctx.start.getTokenIndex());
        	for(Field field : ctx.getClass().getDeclaredFields())
        	{
        		for (int i = 0; i < ctx.getChildCount(); i++) {
        			try {
        				if ( ctx.getChild(i) instanceof TerminalNode ) {
        					Token symbol = ((TerminalNode) ctx.getChild(i)).getSymbol();
        					if (field.get(ctx).equals(symbol)) {
        						jsonStack.peek().put(field.getName(), parser.getVocabulary().getSymbolicName(symbol.getType()));
        						break;
        					}
        				} else if (field.get(ctx).equals(ctx.getChild(i))) {
							jsonStack.peek().put(field.getName(), i);
							break;
						}
					} catch (IllegalArgumentException | IllegalAccessException e) {
					}
        		}
        	}
			jsonStack.peek().put("start", ctx.start.getTokenIndex());
	    	jsonStack.peek().put("stop", ctx.stop.getTokenIndex());
			jsonStack.pop().put("children", childrenStack.pop());
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
//    	System.out.print(ctx.getText());
//    	System.out.println(ctx.toString(this.parser));
//    	System.out.println(ctx.toInfoString(parser));
    }

//	
//	/**
//	 * Enter a parse tree produced by {@link Python3Parser#trailer}.
//	 * @param ctx the parse tree
//	 */
//	public void enterTrailer(Python3Parser.TrailerContext ctx) {
//		System.out.print(ctx.getText());
//	}
//	/**
//	 * Exit a parse tree produced by {@link Python3Parser#trailer}.
//	 * @param ctx the parse tree
//	 */
//	public void exitTrailer(Python3Parser.TrailerContext ctx) {
//		System.out.print(ctx.getText());
//	}

}
