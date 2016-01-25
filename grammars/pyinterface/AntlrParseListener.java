package pyinterface;

import java.io.StringWriter;
import java.lang.reflect.Field;
import java.util.List;
import java.util.Stack;

import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.RuleContext;
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

//    	if (parser.getRuleNames()[ctx.getRuleIndex()].equals("expr")) {
//    		int t =0;
//    	}
//		for (JSONArray c : childrenStack) {
//			System.out.print(c.length());
////    		if (c.length() == 2) {
////    			int t=0;
////    		}
//		}
//		System.out.println();
//		System.out.print("+");
//		System.out.println(ctx.toInfoString(parser));

    	if (!childrenStack.isEmpty()) {
    		this.jsonStack.push(new JSONObject());
    		childrenStack.peek().put(this.jsonStack.peek());
    	}

    	try {
			jsonStack.peek().put("type", parser.getRuleNames()[ctx.getRuleIndex()]);
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

//    public int[] getChildIDFromPointer(ParserRuleContext ctx, Object value) {
//    	if (value != null) {
//	   		for (int i = 0; i < ctx.getChildCount(); i++) {
//				if ( ctx.getChild(i) instanceof TerminalNode ) {
//					Token symbol = ((TerminalNode) ctx.getChild(i)).getSymbol();
//					if (value.equals(symbol)) {
//						return new int[] {1, symbol.getTokenIndex()};
//					}
//				} else if (value.equals(ctx.getChild(i))) {
//					return new int[] {2, i};
//				}
//			}
//    	}
//
//   		return new int[] {0, 0};
//    }

    public int getChildIDFromPointer(RuleContext ctx, Object value) {
    	if (value != null) {
	   		for (int i = 0; i < ctx.getChildCount(); i++) {
				if ( ctx.getChild(i) instanceof TerminalNode ) {
					Token symbol = ((TerminalNode) ctx.getChild(i)).getSymbol();
					if (value == symbol) {
						return i;
					}
				} else if (value == ctx.getChild(i)) {
					return i;
				}
			}
    	}

   		return -1;
    }


    public void exitEveryRule(ParserRuleContext ctx) {
//    	System.out.println(parser.getRuleNames()[ctx.getRuleIndex()]);
//    	if (parser.getRuleNames()[ctx.getRuleIndex()].equals("file_input"))
//    	{
//    		int t=0;
//    	}
//		for (JSONArray c : childrenStack) {
//			System.out.print(c.length());
////    		if (c.length() == 2) {
////    			int t=0;
////    		}
//		}
//		System.out.println();
//		System.out.print("-");
//		System.out.println(ctx.toInfoString(parser));


//    	if ((parser.getRuleNames()[ctx.getRuleIndex()].equals("expr"))) {
//    		if (childrenStack.peek().length() == 2) {
//    			int t=0;
//    		}
//    	}

    	try {
    		JSONArray fields = new JSONArray();
//    		jsonStack.peek().put("_fields", ctx.start.getTokenIndex());
        	for(Field field : ctx.getClass().getDeclaredFields())
        	{
                if (field.getName().endsWith("_")) {
                	String fieldName = field.getName().substring(0, field.getName().length()-1);
                    try {

                        if (field.getType().isAssignableFrom(List.class)) {
                            List<Object> list = (List<Object>) field.get(ctx);
                            JSONArray field_ids = new JSONArray ();
                            for (Object value : list) {
                                int ret = getChildIDFromPointer(ctx, value);
                                if (ret >= 0) {
                                    field_ids.put(ret);
                                }
                            }

                            jsonStack.peek().put(fieldName, field_ids);
                            fields.put(fieldName);

                        } else {

                            Object value = field.get(ctx);
//	        			if ((field.getName().equals("attr")) && (value != null)){
//	        				int t=0;
//	        			}

                            int ret = getChildIDFromPointer(ctx, value);
                            if (ret >= 0) {
                                jsonStack.peek().put(fieldName, ret);
                                fields.put(fieldName);
                            }
                        }
                    } catch (IllegalArgumentException | IllegalAccessException e) {
                    }
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
//	    	childrenStack.peek().length()
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
	@Override public void visitTerminal(TerminalNode node) {
		try {
			Token tok = node.getSymbol();
			JSONObject jsTok = new JSONObject();
//			jsTok.put("line", tok.getLine());
//			jsTok.put("start", tok.getStartIndex());
//			jsTok.put("stop", tok.getStopIndex());
//			jsTok.put("channel", tok.getChannel());
			jsTok.put("index", tok.getTokenIndex());
			jsTok.put("type", "tokref");
			jsTok.put("toktype", parser.getVocabulary().getSymbolicName(tok.getType()));
//			jsTok.put("type", parser.getVocabulary().getSymbolicName(tok.getType()));
//			jsTok.put("col", tok.getCharPositionInLine());

			childrenStack.peek().put(jsTok);
		} catch (JSONException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation does nothing.</p>
	 */
	@Override public void visitErrorNode(ErrorNode node) { visitTerminal(node); }
}
