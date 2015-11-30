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

package python3;

import org.antlr.v4.gui.Trees;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.DiagnosticErrorListener;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.atn.PredictionMode;
import org.antlr.v4.runtime.misc.IntervalSet;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Run a lexer/parser combo, optionally printing tree string or generating
 *  postscript file. Optionally taking input file.
 *
 *  $ java org.antlr.v4.runtime.misc.TestRig GrammarName startRuleName
 *        [-tree]
 *        [-tokens] [-gui] [-ps file.ps]
 *        [-trace]
 *        [-diagnostics]
 *        [-SLL]
 *        [input-filename(s)]
 */
public class Main {
	public static final String LEXER_START_RULE_NAME = "tokens";

	protected String grammarName;
	protected String startRuleName;
	protected final List<String> inputFiles = new ArrayList<String>();
	protected boolean printTree = false;
	protected boolean printJson = false;
	JSONObject json = null;
	protected String inputText = null;
	protected boolean gui = false;
	protected String psFile = null;
	protected boolean showTokens = false;
	protected boolean trace = false;
	protected boolean diagnostics = false;
	protected String encoding = null;
	protected boolean SLL = false;

	public Main(String[] args) throws Exception {
		if ( args.length < 2 ) {
			System.err.println("java org.antlr.v4.runtime.misc.TestRig GrammarName startRuleName\n" +
							   "  [-tokens] [-tree] [-gui] [-ps file.ps] [-encoding encodingname]\n" +
							   "  [-trace] [-diagnostics] [-SLL] [-file input-filename]\n"+
							   "  [text]");
			System.err.println("Use startRuleName='tokens' if GrammarName is a lexer grammar.");
			System.err.println("Omitting input-filename makes rig read from stdin.");
			System.out.println(Arrays.toString(args));
			return;
		}
		int i=0;
		grammarName = args[i];
		i++;
		startRuleName = args[i];
		i++;
		while ( i<args.length ) {
			String arg = args[i];
			i++;
			if ( arg.charAt(0)!='-' ) { // input file name
				inputText = arg.replaceAll("\\\\n", "\n");
				continue;
			}
			if ( arg.equals("-tree") ) {
				printTree = true;
			}
			if ( arg.equals("-json") ) {
				printJson = true;
			}
			if ( arg.equals("-file") ) {
				if ( i>=args.length ) {
					System.err.println("missing filename on -file");
					return;
				}
				inputFiles.add(args[i]);
				i++;
			}
			if ( arg.equals("-gui") ) {
				gui = true;
			}
			if ( arg.equals("-tokens") ) {
				showTokens = true;
			}
			else if ( arg.equals("-trace") ) {
				trace = true;
			}
			else if ( arg.equals("-SLL") ) {
				SLL = true;
			}
			else if ( arg.equals("-diagnostics") ) {
				diagnostics = true;
			}
			else if ( arg.equals("-encoding") ) {
				if ( i>=args.length ) {
					System.err.println("missing encoding on -encoding");
					return;
				}
				encoding = args[i];
				i++;
			}
			else if ( arg.equals("-ps") ) {
				if ( i>=args.length ) {
					System.err.println("missing filename on -ps");
					return;
				}
				psFile = args[i];
				i++;
			}
		}
	}

	public static void main(String[] args) throws Exception {
		Main testRig = new Main(args);
 		if(args.length >= 2) {
			testRig.process();
		}
	}

	public void process() throws Exception {
//		System.out.println("exec "+grammarName+"."+startRuleName);
		String lexerName = grammarName+"Lexer";
		ClassLoader cl = Thread.currentThread().getContextClassLoader();
		Class<? extends Lexer> lexerClass = null;
		try {
			lexerClass = cl.loadClass(lexerName).asSubclass(Lexer.class);
		}
		catch (java.lang.ClassNotFoundException cnfe) {
			// might be pure lexer grammar; no Lexer suffix then
			lexerName = grammarName;
			try {
				lexerClass = cl.loadClass(lexerName).asSubclass(Lexer.class);
			}
			catch (ClassNotFoundException cnfe2) {
				System.err.println("Can't load "+lexerName+" as lexer or parser");
				return;
			}
		}

		Constructor<? extends Lexer> lexerCtor = lexerClass.getConstructor(CharStream.class);
		Lexer lexer = lexerCtor.newInstance((CharStream)null);

		Class<? extends Parser> parserClass = null;
		Parser parser = null;
		if ( !startRuleName.equals(LEXER_START_RULE_NAME) ) {
			String parserName = grammarName+"Parser";
			parserClass = cl.loadClass(parserName).asSubclass(Parser.class);
			if ( parserClass==null ) {
				System.err.println("Can't load "+parserName);
			}
			Constructor<? extends Parser> parserCtor = parserClass.getConstructor(TokenStream.class);
			parser = parserCtor.newInstance((TokenStream)null);
		}

		if (inputText != null) {
			Reader r = new StringReader(inputText);
			process(lexer, parserClass, parser, null, r);
		} else if ( inputFiles.size()==0 ) {
			InputStream is = System.in;
			Reader r;
			if ( encoding!=null ) {
				r = new InputStreamReader(is, encoding);
			}
			else {
				r = new InputStreamReader(is);
			}

			process(lexer, parserClass, parser, is, r);
		} else {
			for (String inputFile : inputFiles) {
				InputStream is = System.in;
				if ( inputFile!=null ) {
					is = new FileInputStream(inputFile);
				}
				Reader r;
				if ( encoding!=null ) {
					r = new InputStreamReader(is, encoding);
				}
				else {
					r = new InputStreamReader(is);
				}
	
				if ( inputFiles.size()>1 ) {
					System.err.println(inputFile);
				}
				process(lexer, parserClass, parser, is, r);
			}
		}
	}

	protected void process(Lexer lexer, Class<? extends Parser> parserClass, Parser parser, InputStream is, Reader r) throws IOException, IllegalAccessException, InvocationTargetException, PrintException {
		try {
			ANTLRInputStream input = new ANTLRInputStream(r);
			lexer.setInputStream(input);
			CommonTokenStream tokens = new CommonTokenStream(lexer);

			tokens.fill();

			if ( showTokens ) {
				for (Object tok : tokens.getTokens()) {
					System.out.println(tok);
				}
			}

			if ( startRuleName.equals(LEXER_START_RULE_NAME) ) return;

			if ( diagnostics ) {
				parser.addErrorListener(new DiagnosticErrorListener());
				parser.getInterpreter().setPredictionMode(PredictionMode.LL_EXACT_AMBIG_DETECTION);
			}
			
			if ( printJson ) {
				this.json = new JSONObject();
				JSONObject jsTree = new JSONObject();
				JSONArray jsTokens = new JSONArray();
	
				try {
					json.put("tree", jsTree);
					json.put("tokens", jsTokens);
					for (Token tok : tokens.getTokens()) {
						JSONObject jsTok = new JSONObject();
						jsTok.put("line", tok.getLine());
						jsTok.put("start", tok.getStartIndex());
						jsTok.put("stop", tok.getStopIndex());
						jsTok.put("channel", tok.getChannel());
						jsTok.put("type", parser.getVocabulary().getSymbolicName(tok.getType()));
						jsTok.put("col", tok.getCharPositionInLine());
						jsTokens.put(jsTok);
					}
	
				} catch (JSONException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

				parser.addParseListener(new Python3ParseListener((Python3Parser) parser, jsTree));
			}

			if ( printTree || gui || psFile!=null ) {
				parser.setBuildParseTree(true);
			}

			if ( SLL ) { // overrides diagnostics
				parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
			}

			parser.setTokenStream(tokens);
			parser.setTrace(trace);

			try {
				Method startRule = parserClass.getMethod(startRuleName);
				ParserRuleContext tree = (ParserRuleContext)startRule.invoke(parser, (Object[])null);

				if ( printJson ) {
					StringWriter out = new StringWriter();
					try {
						json.write(out);
					} catch (JSONException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					System.out.println(out.toString());
				}
				if ( printTree ) {
					System.out.println(tree.toStringTree(parser));
				}
				if ( gui ) {
					Trees.inspect(tree, parser);
				}
				if ( psFile!=null ) {
					Trees.save(tree, parser, psFile); // Generate postscript
				}
			}
			catch (NoSuchMethodException nsme) {
				System.err.println("No method for rule "+startRuleName+" or it has arguments");
			}
		}
		finally {
			if ( r!=null ) r.close();
			if ( is!=null ) is.close();
		}
	}
}
//
//
///** Run a lexer/parser combo, optionally printing tree string or generating
// *  postscript file. Optionally taking input file.
// *
// *  $ java org.antlr.v4.runtime.misc.TestRig GrammarName startRuleName
// *        [-tree]
// *        [-tokens] [-gui] [-ps file.ps]
// *        [-trace]
// *        [-diagnostics]
// *        [-SLL]
// *        [input-filename(s)]
// */
//public class Main {
//	public static final String LEXER_START_RULE_NAME = "tokens";
//
//	protected String grammarName;
//	protected String startRuleName;
//	protected final List<String> inputFiles = new ArrayList<String>();
//	protected boolean printTree = false;
//	protected boolean gui = false;
//	protected String psFile = null;
//	protected boolean showTokens = false;
//	protected boolean trace = false;
//	protected boolean diagnostics = true;
//	protected String encoding = null;
//	protected boolean SLL = false;
//
//	public Main(String[] args) throws Exception {
//		if ( args.length < 2 ) {
//			System.err.println("java org.antlr.v4.runtime.misc.TestRig GrammarName startRuleName\n" +
//							   "  [-tokens] [-tree] [-gui] [-ps file.ps] [-encoding encodingname]\n" +
//							   "  [-trace] [-diagnostics] [-SLL]\n"+
//							   "  [input-filename(s)]");
//			System.err.println("Use startRuleName='tokens' if GrammarName is a lexer grammar.");
//			System.err.println("Omitting input-filename makes rig read from stdin.");
//			return;
//		}
//		int i=0;
//		grammarName = args[i];
//		i++;
//		startRuleName = args[i];
//		i++;
//		while ( i<args.length ) {
//			String arg = args[i];
//			i++;
//			if ( arg.charAt(0)!='-' ) { // input file name
//				inputFiles.add(arg);
//				continue;
//			}
//			if ( arg.equals("-tree") ) {
//				printTree = true;
//			}
//			if ( arg.equals("-gui") ) {
//				gui = true;
//			}
//			if ( arg.equals("-tokens") ) {
//				showTokens = true;
//			}
//			else if ( arg.equals("-trace") ) {
//				trace = true;
//			}
//			else if ( arg.equals("-SLL") ) {
//				SLL = true;
//			}
//			else if ( arg.equals("-diagnostics") ) {
//				diagnostics = true;
//			}
//			else if ( arg.equals("-encoding") ) {
//				if ( i>=args.length ) {
//					System.err.println("missing encoding on -encoding");
//					return;
//				}
//				encoding = args[i];
//				i++;
//			}
//			else if ( arg.equals("-ps") ) {
//				if ( i>=args.length ) {
//					System.err.println("missing filename on -ps");
//					return;
//				}
//				psFile = args[i];
//				i++;
//			}
//		}
//	}
//
//	public static void main(String[] args) throws Exception {
//		Main testRig = new Main(args);
// 		if(args.length >= 2) {
//			testRig.process();
//		}
//	}
//
//	public void process() throws Exception {
////		System.out.println("exec "+grammarName+"."+startRuleName);
////		String lexerName = grammarName+"Lexer";
////		ClassLoader cl = Thread.currentThread().getContextClassLoader();
////		Class<? extends Lexer> lexerClass = null;
////		try {
////			lexerClass = cl.loadClass(lexerName).asSubclass(Lexer.class);
////		}
////		catch (java.lang.ClassNotFoundException cnfe) {
////			// might be pure lexer grammar; no Lexer suffix then
////			lexerName = grammarName;
////			try {
////				lexerClass = cl.loadClass(lexerName).asSubclass(Lexer.class);
////			}
////			catch (ClassNotFoundException cnfe2) {
////				System.err.println("Can't load "+lexerName+" as lexer or parser");
////				return;
////			}
////		}
////
////		Constructor<? extends Lexer> lexerCtor = lexerClass.getConstructor(CharStream.class);
//		Lexer lexer = new Python3Lexer((CharStream)null);
//
////		Class<? extends Parser> parserClass = null;
//		Parser parser = null;
//		if ( !startRuleName.equals(LEXER_START_RULE_NAME) ) {
//			parser = new Python3Parser((TokenStream)null);
////			String parserName = grammarName+"Parser";
////			parserClass = cl.loadClass(parserName).asSubclass(Parser.class);
////			if ( parserClass==null ) {
////				System.err.println("Can't load "+parserName);
////			}
////			Constructor<? extends Parser> parserCtor = parserClass.getConstructor(TokenStream.class);
////			parser = parserCtor.newInstance((TokenStream)null);
//		}
//
//		if ( inputFiles.size()==0 ) {
//			InputStream is = System.in;
//			Reader r;
//			if ( encoding!=null ) {
//				r = new InputStreamReader(is, encoding);
//			}
//			else {
//				r = new InputStreamReader(is);
//			}
//
//			process(lexer, Python3Parser.class, parser, is, r);
//			return;
//		}
//		for (String inputFile : inputFiles) {
//			InputStream is = System.in;
//			if ( inputFile!=null ) {
//				is = new FileInputStream(inputFile);
//			}
//			Reader r;
//			if ( encoding!=null ) {
//				r = new InputStreamReader(is, encoding);
//			}
//			else {
//				r = new InputStreamReader(is);
//			}
//
//			if ( inputFiles.size()>1 ) {
//				System.err.println(inputFile);
//			}
//			process(lexer, Python3Parser.class, parser, is, r);
//		}
//	}
//
//	protected void process(Lexer lexer, Class<? extends Parser> parserClass, Parser parser, InputStream is, Reader r) throws IOException, IllegalAccessException, InvocationTargetException, PrintException {
//		try {
//			ANTLRInputStream input = new ANTLRInputStream(r);
//			lexer.setInputStream(input);
//			CommonTokenStream tokens = new CommonTokenStream(lexer);
//
//			tokens.fill();
//
//			if ( showTokens ) {
//				for (Object tok : tokens.getTokens()) {
//					System.out.println(tok);
//				}
//			}
//
//			if ( startRuleName.equals(LEXER_START_RULE_NAME) ) return;
//
//			JSONObject json = new JSONObject();
//			JSONObject jsTree = new JSONObject();
//			JSONArray jsTokens = new JSONArray();
//
//			try {
//				json.put("tree", jsTree);
//				json.put("tokens", jsTokens);
//				for (Token tok : tokens.getTokens()) {
//					JSONObject jsTok = new JSONObject();
//					jsTok.put("line", tok.getLine());
//					jsTok.put("start", tok.getStartIndex());
//					jsTok.put("stop", tok.getStopIndex());
//					jsTok.put("channel", tok.getChannel());
//					jsTok.put("type", parser.getVocabulary().getSymbolicName(tok.getType()));
//					jsTok.put("col", tok.getCharPositionInLine());
//					jsTokens.put(jsTok);
//				}
//
//			} catch (JSONException e1) {
//				// TODO Auto-generated catch block
//				e1.printStackTrace();
//			}
//			
//			if ( diagnostics ) {
////				parser.removeErrorListeners();
////				parser.setErrorHandler(new Python3ErrorStrategy());
////				parser.addErrorListener(new PythonErrorListener());
//				
//				parser.addParseListener(new Python3ParseListener((Python3Parser) parser, jsTree));
//				parser.getInterpreter().setPredictionMode(PredictionMode.LL_EXACT_AMBIG_DETECTION);
//			}
//
//			if ( printTree || gui || psFile!=null ) {
//				parser.setBuildParseTree(true);
//			}
//
//			if ( SLL ) { // overrides diagnostics
//				parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
//			}
//
//			parser.setTokenStream(tokens);
//			parser.setTrace(trace);
//
//			try {
//				Method startRule = parserClass.getMethod(startRuleName);
//				ParserRuleContext tree = (ParserRuleContext)startRule.invoke(parser, (Object[])null);
//				
//				StringWriter out = new StringWriter();
//				try {
//					json.write(out);
//				} catch (JSONException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//			   String jsonText = out.toString();
//			   PrintWriter fout = new PrintWriter("parse.js");
//			   fout.print(jsonText);
//			   fout.close();
////				IntervalSet bla = parser.getExpectedTokens();
//				if ( printTree ) {
//					System.out.println(tree.toStringTree(parser));
//				}
//				if ( gui ) {
//					Trees.inspect(tree, parser);
//				}
//				if ( psFile!=null ) {
//					Trees.save(tree, parser, psFile); // Generate postscript
//				}
//			}
//			catch (NoSuchMethodException nsme) {
//				System.err.println("No method for rule "+startRuleName+" or it has arguments");
//			}
//		}
//		finally {
//			if ( r!=null ) r.close();
//			if ( is!=null ) is.close();
//		}
//	}
//}
//
