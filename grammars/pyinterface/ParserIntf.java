package pyinterface;

import java.lang.reflect.Constructor;
import java.util.Arrays;
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
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import sun.misc.IOUtils;

//import org.apache.commons.io.IOUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringReader;
import java.io.StringWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import javax.print.PrintException;

public class ParserIntf {
	public static final String LEXER_START_RULE_NAME = "tokens";

	protected String grammarName;
	protected String startRuleName;
	JSONObject json = null;
	Lexer lexer;
	Class<? extends Parser> parserClass;
	Parser parser;

	public ParserIntf(String[] args) throws Exception {
		if ( args.length < 2 ) {
			System.err.println("java pyinterface.ParserIntf GrammarName startRuleName");
			System.out.println(Arrays.toString(args));
			return;
		}
		grammarName = args[0];
		startRuleName = args[1];
		
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
		lexer = lexerCtor.newInstance((CharStream)null);

		parserClass = null;
		parser = null;
		if ( !startRuleName.equals(LEXER_START_RULE_NAME) ) {
			String parserName = grammarName+"Parser";
			parserClass = cl.loadClass(parserName).asSubclass(Parser.class);
			if ( parserClass==null ) {
				System.err.println("Can't load "+parserName);
			}
			Constructor<? extends Parser> parserCtor = parserClass.getConstructor(TokenStream.class);
			parser = parserCtor.newInstance((TokenStream)null);
		}
	}
	
	public static void main(String[] args) throws Exception {
		ParserIntf parserIntf = new ParserIntf(args);
 		if(args.length >= 2) {
 			while(true) {
 				parserIntf.process();
 			}
		}
	}

	public void process() throws Exception {
//		System.out.println("exec "+grammarName+"."+startRuleName);
		
		byte[] inputEncoded = IOUtils.readFully(System.in, -1, true);
		String inputText = new String(inputEncoded);
//		System.out.println("RECEIVED:");
//		System.out.print(inputText);
//		System.out.println("END_RECEIVED;");
		Reader r = new StringReader(inputText);
		
//        Reader r = new StringReader(inputText);
		process(lexer, parserClass, parser, r);
	}
	
	protected void process(Lexer lexer, Class<? extends Parser> parserClass, Parser parser, Reader r) throws IOException, IllegalAccessException, InvocationTargetException, PrintException {
		try {
			ANTLRInputStream input = new ANTLRInputStream(r);
			lexer.setInputStream(input);
			CommonTokenStream tokens = new CommonTokenStream(lexer);

			tokens.fill();

			if ( startRuleName.equals(LEXER_START_RULE_NAME) ) return;
			
			parser.setBuildParseTree(true);

			parser.setTokenStream(tokens);

			try {
				Method startRule = parserClass.getMethod(startRuleName);
				ParserRuleContext tree = (ParserRuleContext)startRule.invoke(parser, (Object[])null);
				
				ParseTreeWalker walker = new ParseTreeWalker(); // create standard walker

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
						jsTok.put("index", tok.getTokenIndex());
						if (tok.getStartIndex() <= tok.getStopIndex()) {
							jsTok.put("text", tok.getText());
						} else {
							jsTok.put("text", "");
						}
						jsTok.put("type", parser.getVocabulary().getSymbolicName(tok.getType()));
						jsTok.put("col", tok.getCharPositionInLine());
						jsTokens.put(jsTok);
					}
	
				} catch (JSONException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

//				parser.addParseListener(new AntlrParseListener(parser, jsTree));


				AntlrParseListener listener = new AntlrParseListener(parser, jsTree);
				walker.walk(listener, tree); // initiate walk of tree with listener

				StringWriter out = new StringWriter();
				try {
					json.write(out);
				} catch (JSONException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				System.out.println(out.toString());
			}
			catch (NoSuchMethodException nsme) {
				System.err.println("No method for rule "+startRuleName+" or it has arguments");
			}
		}
		finally {
//			if ( r!=null ) r.close();
//			if ( is!=null ) is.close();
		}
	}
}


