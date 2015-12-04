package pyinterface;

import java.io.StringWriter;
import java.lang.reflect.Field;
import java.util.List;
import java.util.Stack;

import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ErrorNode;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;
import org.antlr.v4.runtime.tree.ParseTreeListener;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;

public class AntlrParseListener implements ParseTreeListener {
	Parser parser;
	JSONObject jsonTop;
	Stack<JSONArray> childrenStack = new Stack<JSONArray>();
	Stack<JSONObject> jsonStack = new Stack<JSONObject>();
	
	public AntlrParseListener(Parser parser, JSONObject json) {
        this.parser = parser;
        this.jsonStack.push(json);
    }
	
    public void enterEveryRule(ParserRuleContext ctx) {
//    	System.out.print(ctx.toString(this.parser));
//    	System.out.print(" ");
//    	System.out.println(ctx.toInfoString(parser));

    	if (parser.getRuleNames()[ctx.getRuleIndex()].equals("power")) {
    		assert true;
    	}
    	
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
    
    public int[] getChildIDFromPointer(ParserRuleContext ctx, Object value) {
    	if (value != null) {
	   		for (int i = 0; i < ctx.getChildCount(); i++) {
				if ( ctx.getChild(i) instanceof TerminalNode ) {
					Token symbol = ((TerminalNode) ctx.getChild(i)).getSymbol();
					if (value.equals(symbol)) {
						return new int[] {1, symbol.getTokenIndex()};
					}
				} else if (value.equals(ctx.getChild(i))) {
					return new int[] {2, i};
				}
			}
    	}
  		
   		return new int[] {0, 0};
    }
    
    public void exitEveryRule(ParserRuleContext ctx) {
    	try {
    		JSONArray fields = new JSONArray();
//    		jsonStack.peek().put("_fields", ctx.start.getTokenIndex());
        	for(Field field : ctx.getClass().getDeclaredFields())
        	{
        		try {
	        		
	        		if (field.getType().isAssignableFrom(List.class)) {
	        			List<Object> list = (List<Object>) field.get(ctx);
	        			JSONArray field_ids = new JSONArray ();
	        			for (Object value : list) {
		        			int[] ret = getChildIDFromPointer(ctx, value);
		        			if (ret[0] == 1) {
		        				field_ids.put(String.format("%d", ret[1]));
		        			} else if (ret[0] == 2) {
		        				field_ids.put(ret[1]);
		        			}
	        			}

	        			jsonStack.peek().put(field.getName(), field_ids);
		        		fields.put(field.getName());

	        		} else {
	        			Object value = field.get(ctx);
	        			int[] ret = getChildIDFromPointer(ctx, value);
	        			if (ret[0] == 1) {
	        				jsonStack.peek().put(field.getName(), String.format("%d", ret[1]));
	        				fields.put(field.getName());
	        			} else if (ret[0] == 2) {
	        				jsonStack.peek().put(field.getName(), ret[1]);
	        				fields.put(field.getName());
	        			}
	        		}
	        	} catch (IllegalArgumentException | IllegalAccessException e) {
        		}
//	        			
//	        		
//	        		
//	        		
//	        		if (value != null) {
//		        		for (int i = 0; i < ctx.getChildCount(); i++) {
//	        				if ( ctx.getChild(i) instanceof TerminalNode ) {
//	        					Token symbol = ((TerminalNode) ctx.getChild(i)).getSymbol();
//	        					if (value.equals(symbol)) {
////	        						jsonStack.peek().put(field.getName(), parser.getVocabulary().getSymbolicName(symbol.getType()));
//	        						break;
//	        					}
//	        				} else if (field.get(ctx).equals(ctx.getChild(i))) {
//
//								break;
//							}
//		        		}
//	        		}
//        		} catch (IllegalArgumentException | IllegalAccessException e) {
//        		}
        	}
        	jsonStack.peek().put("_fields", fields);
			jsonStack.peek().put("start", ctx.start.getTokenIndex());
	    	jsonStack.peek().put("stop", ctx.stop.getTokenIndex());
	    	jsonStack.peek().put("grammar", parser.getGrammarFileName());
			jsonStack.pop().put("children", childrenStack.pop());
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
//    	System.out.print(ctx.getText());
//    	System.out.println(ctx.toString(this.parser));
//    	System.out.println(ctx.toInfoString(parser));
    }

    /**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation does nothing.</p>
	 */
	@Override public void visitTerminal(TerminalNode node) { }
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation does nothing.</p>
	 */
	@Override public void visitErrorNode(ErrorNode node) { }
}
