/*
 * [The "BSD license"]
 *  Copyright (c) 2012 Terence Parr
 *  Copyright (c) 2012 Sam Harwell
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 *  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 *  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 *  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package pyinterface;

import java.util.BitSet;
import java.util.Collections;

import org.antlr.v4.gui.Trees;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.DiagnosticErrorListener;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.LexerInterpreter;
import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserInterpreter;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Recognizer;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.atn.DecisionInfo;
import org.antlr.v4.runtime.atn.LookaheadEventInfo;
import org.antlr.v4.runtime.atn.PredictionMode;
import org.antlr.v4.runtime.misc.IntervalSet;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.antlr.v4.tool.Grammar;
import org.antlr.v4.tool.GrammarParserInterpreter;
import org.antlr.v4.tool.LexerGrammar;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import linpath.linpathParser;
import linpath.linpathLexer;

import javax.print.PrintException;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringBufferInputStream;
import java.io.StringReader;
import java.io.StringWriter;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.antlr.runtime.RecognitionException;
import org.antlr.v4.Tool;

public class CompletionMain {
	public static final String lexerText =
		"lexer grammar L;\n" +
		"DOT  : '.' ;\n" +
		"SEMI : ';' ;\n" +
		"BANG : '!' ;\n" +
		"PLUS : '+' ;\n" +
		"LPAREN : '(' ;\n" +
		"RPAREN : ')' ;\n" +
		"MULT : '*' ;\n" +
		"ID : [a-z]+ ;\n" +
		"INT : [0-9]+ ;\n" +
		"WS : [ \\r\\t\\n]+ ;\n";

	public CompletionMain(String[] args) throws Exception {
	}

	public static void main(String[] args) throws Exception {
		CompletionMain testRig = new CompletionMain(args);
		//testRig.process();
		//testRig.testLinpathParser("a/b/", "main", 1);
		testRig.testLinpathCompletion("a/b/", "main", 1);
	}

	public void testAlts() throws Exception {
//		LexerGrammar lg = new LexerGrammar(lexerText);
		LexerGrammar lg = new LexerGrammar(
			"lexer grammar L;\n" +
			"ID : [0-9a-zA-Z_]+ ;\n" + 
			"PATHSEP :'/' ;\n");
		Grammar g = new Grammar(
			"parser grammar T;\n" +
			"s : e_=e EOF ;\n" +	// 
			"e : id_+=ID (sep_=PATHSEP id_+=ID)* folder_=PATHSEP?\n"+
			//"  | ID (DOT ID)* DOT? \n"+ //LPAREN RPAREN\n"+
			"  ;\n",
			lg);

		String startRuleName = "s";
		int decision = 2;

		testLookaheadTrees(lg, g, "a/b/", startRuleName, decision,
						   new String[] {"(e:1 a . b)", "(e:2 a <error .>)"});
	}

	/**
	 * @param lg
	 * @param g
	 * @param input
	 * @param startRuleName
	 * @param decision
	 * @param expectedTrees
	 */
	public void testLookaheadTrees(LexerGrammar lg, Grammar g,
								   String input,
								   String startRuleName,	// 
								   int decision,
								   String[] expectedTrees)
	{
		
		int startRuleIndex = g.getRule(startRuleName).index;
//		InterpreterTreeTextProvider nodeTextProvider =
//					new InterpreterTreeTextProvider(g.getRuleNames());
		
		LexerInterpreter lexEngine = lg.createLexerInterpreter(new ANTLRInputStream(input));
		CommonTokenStream tokens = new CommonTokenStream(lexEngine);
		GrammarParserInterpreter parser = g.createGrammarParserInterpreter(tokens);
		parser.removeErrorListeners();
//		parser.addErrorListener(new VerboseListener());
		parser.setProfile(true);
		ParseTree t = parser.parse(startRuleIndex);

		DecisionInfo decisionInfo = parser.getParseInfo().getDecisionInfo()[decision];
		LookaheadEventInfo lookaheadEventInfo = decisionInfo.SLL_MaxLookEvent;

//		List<ParserRuleContext> lookaheadParseTrees =
//			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
//															lookaheadEventInfo.startIndex, lookaheadEventInfo.stopIndex);

		List<ParserRuleContext> lookaheadParseTrees =
			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
															3,3);

		
		for (int i = 0; i < lookaheadParseTrees.size(); i++) {
			ParserRuleContext lt = lookaheadParseTrees.get(i);
//			System.out.println("parse tree: "+Trees.toStringTree(lt, nodeTextProvider));
//			assertEquals(expectedTrees[i], Trees.toStringTree(lt, nodeTextProvider));
		}
	}
	

	public void testLinpathCompletion( String input,
								   String startRuleName,	// 
								   int decision
								   ) throws RecognitionException, IOException
	{
		input = "";
		
		int caretIndex = 1;
		Grammar g = new Grammar(new String(Files.readAllBytes(Paths.get("/home/bvukobratovic/projects/pyde/grammars/linpath/linpath_test.g4"))));
		
		GrammarASTJson js = new GrammarASTJson(g);
		JSONObject rules = js.toJson();
		int startRuleIndex = g.getRule(startRuleName).index;
		
		linpathLexer lexEngine = new linpathLexer(new ANTLRInputStream(input));
		CommonTokenStream tokens = new CommonTokenStream(lexEngine); 

		CompletionGrammarParserInterpreter parser = new CompletionGrammarParserInterpreter(g, tokens);
		
		JSONArray s = parser.getSuggestions(g, startRuleIndex, caretIndex);
		System.out.println(s);
	}
	
	public void testLinpathParser( String input,
								   String startRuleName,	// 
								   int decision
								   ) throws RecognitionException, IOException
	{
		Grammar g = new Grammar(new String(Files.readAllBytes(Paths.get("/home/bvukobratovic/projects/pyde/grammars/linpath/linpath_test.g4"))));
		
		GrammarASTJson js = new GrammarASTJson(g);
		JSONObject rules = js.toJson();
		int startRuleIndex = g.getRule(startRuleName).index;
//		InterpreterTreeTextProvider nodeTextProvider =
//					new InterpreterTreeTextProvider(g.getRuleNames());

		linpathLexer lexEngine = new linpathLexer(new ANTLRInputStream(input));
		CommonTokenStream tokens = new CommonTokenStream(lexEngine);	// 
		
		//LexerInterpreter lexEngine = lg.createLexerInterpreter(new ANTLRInputStream(input));
		GrammarParserInterpreter parser = g.createGrammarParserInterpreter(tokens);
		parser.setProfile(true);
		ParseTree t = parser.parse(startRuleIndex);

		DecisionInfo decisionInfo = parser.getParseInfo().getDecisionInfo()[decision];
		LookaheadEventInfo lookaheadEventInfo = decisionInfo.SLL_MaxLookEvent;

//		List<ParserRuleContext> lookaheadParseTrees =
//			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
//															lookaheadEventInfo.startIndex, lookaheadEventInfo.stopIndex);

		List<ParserRuleContext> lookaheadParseTrees =
			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
															3,3);

		
		for (int i = 0; i < lookaheadParseTrees.size(); i++) {
			ParserRuleContext lt = lookaheadParseTrees.get(i);
//			System.out.println("parse tree: "+Trees.toStringTree(lt, nodeTextProvider));
//			assertEquals(expectedTrees[i], Trees.toStringTree(lt, nodeTextProvider));
		}
	}
	
	public void process() throws Exception {
		LexerGrammar lg = new LexerGrammar(
			"lexer grammar L;\n" +
			"ID : [0-9a-zA-Z_]+ ;\n" + 
			"PATHSEP :'/' ;\n");
		Grammar g = new Grammar(
			"parser grammar T;\n" +
			"path :   ID (PATHSEP ID)* " + 
			"       | ID (PATHSEP ID)* folder? ;\n" + 
			"folder : PATHSEP;",
			lg);

		String input = "root/sub/";
		String startRuleName = "path";
		int decision = 1;
		
//		LexerInterpreter lexEngine = lg.createLexerInterpreter(new ANTLRInputStream(input));
//		CommonTokenStream tokens = new CommonTokenStream(lexEngine);
//		CompletionParserInterpreter parser = g.createParserInterpreter(tokens);
//		ParseTree t = parser.parse(g.rules.get(startRule).index);
//		System.out.println("parse tree: "+t.toStringTree(parser));
////		assertEquals(expectedParseTree, t.toStringTree(parser));

		int startRuleIndex = g.getRule(startRuleName).index;
//		InterpreterTreeTextProvider nodeTextProvider =
//					new InterpreterTreeTextProvider(g.getRuleNames());

		LexerInterpreter lexEngine = lg.createLexerInterpreter(new ANTLRInputStream(input));
		CommonTokenStream tokens = new CommonTokenStream(lexEngine);
		GrammarParserInterpreter parser = g.createGrammarParserInterpreter(tokens);
		parser.setProfile(true);
		ParseTree t = parser.parse(startRuleIndex);
		BitSet b = parser.findOuterMostDecisionStates();

		DecisionInfo decisionInfo = parser.getParseInfo().getDecisionInfo()[decision];
		LookaheadEventInfo lookaheadEventInfo = decisionInfo.SLL_MaxLookEvent;

		List<ParserRuleContext> lookaheadParseTrees =
			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
															lookaheadEventInfo.startIndex, lookaheadEventInfo.stopIndex);

//		List<ParserRuleContext> lookaheadParseTrees =
//			GrammarParserInterpreter.getLookaheadParseTrees(g, parser, tokens, startRuleIndex, lookaheadEventInfo.decision,
//															1, 3);

		
//		assertEquals(expectedTrees.length, lookaheadParseTrees.size());
		for (int i = 0; i < lookaheadParseTrees.size(); i++) {
			ParserRuleContext lt = lookaheadParseTrees.get(i);
//			System.out.println("parse tree: "+Trees.toStringTree(lt, nodeTextProvider));
//			assertEquals(expectedTrees[i], Trees.toStringTree(lt, nodeTextProvider));
		}

		
	}
}
