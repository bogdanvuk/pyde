package pyinterface;

import java.util.ArrayList;
import java.util.List;

import org.antlr.v4.runtime.ANTLRErrorStrategy;
import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserInterpreter;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.Recognizer;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.atn.ATN;
import org.antlr.v4.runtime.atn.ATNDeserializer;
import org.antlr.v4.runtime.atn.ATNSerializer;
import org.antlr.v4.runtime.atn.DecisionInfo;
import org.antlr.v4.runtime.atn.DecisionState;
import org.antlr.v4.runtime.atn.LookaheadEventInfo;
import org.antlr.v4.runtime.tree.Trees;
import org.antlr.v4.tool.Grammar;
import org.antlr.v4.tool.GrammarParserInterpreter;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class CompletionGrammarParserInterpreter extends GrammarParserInterpreter {
	JSONArray suggestions;
	CompletionErrorListener errListener;
	
	public static class CompletionErrorStrategy extends BailButConsumeErrorStrategy {
		JSONArray suggestions;
		
		public CompletionErrorStrategy() {
			suggestions = new JSONArray();
		}
		
		@Override
		public void recover(Parser recognizer, RecognitionException e) {
			GrammarParserInterpreter r = (GrammarParserInterpreter) recognizer;
			if (r.getContext().invokingState >= 0) {
				JSONObject s = new JSONObject();
				suggestions.put(s);
				try {
					JSONArray stateStack = new JSONArray();
					stateStack.put(e.getOffendingState());
					ParserRuleContext ctx = r.getContext();
					while (ctx != null){
						if (ctx.invokingState >= 0) {
							stateStack.put(ctx.invokingState);
						}
						ctx = ctx.getParent();
					}
					s.put("state_stack", stateStack);
					s.put("rule", r.getVocabulary().getSymbolicName(r.getContext().getRuleIndex()));
				} catch (JSONException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			}
			super.recover(recognizer, e);
		}
	}
	
	public static class CompletionErrorListener extends BaseErrorListener {
		JSONArray suggestions;
		
		public CompletionErrorListener() {
			suggestions = new JSONArray();
		}

		public void syntaxError(Recognizer<?,?> recognizer,
               Object offendingSymbol,
               int line,
               int charPositionInLine,
               String msg,
               RecognitionException e) {
			GrammarParserInterpreter r = (GrammarParserInterpreter) recognizer;
			if (r.getContext().invokingState >= 0) {
				JSONObject s = new JSONObject();
				suggestions.put(s);
				try {
					JSONArray stateStack = new JSONArray();
					stateStack.put(e.getOffendingState());
					ParserRuleContext ctx = r.getContext();
					while (ctx != null){
						if (ctx.invokingState >= 0) {
							stateStack.put(ctx.invokingState);
						}
						ctx = ctx.getParent();
					}
					s.put("state_stack", stateStack);
					s.put("rule", r.getVocabulary().getSymbolicName(r.getContext().getRuleIndex()));
				} catch (JSONException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			}
		}
	}
	
	public CompletionGrammarParserInterpreter(Grammar g, TokenStream input) {
		super(g, 
			new ATNDeserializer().deserialize(ATNSerializer.getSerializedAsChars(g.atn)), 
			input);
		errListener = new CompletionErrorListener();
		this.addErrorListener(errListener);
	}
	
	public CompletionGrammarParserInterpreter(Grammar g, ATN atn, TokenStream input) {
		super(g, atn, input);
	}
	
	public JSONArray getSuggestions(Grammar g,
			int startRuleIndex,
			int caretIndex
			) {
//		InterpreterTreeTextProvider nodeTextProvider =
//			new InterpreterTreeTextProvider(g.getRuleNames());

		this.setProfile(true);
		this.parse(startRuleIndex);

		suggestions = new JSONArray();
		for (DecisionInfo decisionInfo: this.getParseInfo().getDecisionInfo()) {
			LookaheadEventInfo lookaheadEventInfo = decisionInfo.SLL_MaxLookEvent;
			if (lookaheadEventInfo != null) {
//			if ((lookaheadEventInfo.startIndex <= caretIndex) &&
//					(lookaheadEventInfo.stopIndex >= caretIndex)) {
				//System.out.format("d: %d, start: %d, stop: %d\n", lookaheadEventInfo.decision, lookaheadEventInfo.startIndex, lookaheadEventInfo.stopIndex);
				List<ParserRuleContext> lookaheadParseTrees =
						CompletionGrammarParserInterpreter.getLookaheadParseTrees(g, 
								this, 
								this.getTokenStream(), 
								startRuleIndex, 
								lookaheadEventInfo.decision,
								caretIndex,
//								caretIndex);
//								lookaheadEventInfo.startIndex,
								caretIndex);
//								lookaheadEventInfo.stopIndex);
//				for (int i = 0; i < lookaheadParseTrees.size(); i++) {
//					ParserRuleContext lt = lookaheadParseTrees.get(i);
//					System.out.println("parse tree: "+org.antlr.v4.gui.Trees.toStringTree(lt, nodeTextProvider));
//				}
			}
		}
		for (int i = 0; i < errListener.suggestions.length(); i++) {
			try {
				suggestions.put(errListener.suggestions.get(i));
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}

		return suggestions;
	}

	public static List<ParserRuleContext> getLookaheadParseTrees(Grammar g,
																 CompletionGrammarParserInterpreter originalParser,
																 TokenStream tokens,
																 int startRuleIndex,
																 int decision,
																 int startIndex,
																 int stopIndex)
	{
		List<ParserRuleContext> trees = new ArrayList<ParserRuleContext>();
		// Create a new parser interpreter to parse the ambiguous subphrase
		ParserInterpreter parser = deriveTempParserInterpreter(g, originalParser, tokens);
		CompletionErrorStrategy errorHandler = new CompletionErrorStrategy();
		parser.setErrorHandler(errorHandler);

		DecisionState decisionState = originalParser.getATN().decisionToState.get(decision);

		for (int alt=1; alt<=decisionState.getTransitions().length; alt++) {
			// re-parse entire input for all ambiguous alternatives
			// (don't have to do first as it's been parsed, but do again for simplicity
			//  using this temp parser.)
			parser.reset();
			parser.addDecisionOverride(decision, startIndex, alt);
			ParserRuleContext tt = parser.parse(startRuleIndex);
			int stopTreeAt = stopIndex;
			if ( errorHandler.firstErrorTokenIndex>=0 ) {
				stopTreeAt = errorHandler.firstErrorTokenIndex; // cut off rest at first error
			}
			ParserRuleContext subtree =
				Trees.getRootOfSubtreeEnclosingRegion(tt,
													  startIndex,
													  stopTreeAt);
			// Use higher of overridden decision tree or tree enclosing all tokens
			if ( Trees.isAncestorOf(parser.getOverrideDecisionRoot(), subtree) ) {
				subtree = parser.getOverrideDecisionRoot();
			}
			Trees.stripChildrenOutOfRange(subtree, parser.getOverrideDecisionRoot(), startIndex, stopTreeAt);
			trees.add(subtree);
		}
		
		for (int i = 0; i < errorHandler.suggestions.length(); i++) {
			try {
				originalParser.suggestions.put(errorHandler.suggestions.get(i));
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}

		
		return trees;
	}
}
