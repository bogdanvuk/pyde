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
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringReader;
import java.io.StringWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import javax.print.PrintException;

public class ParserIntf {
	public static final String LEXER_START_RULE_NAME = "tokens";
	
	static FileInputStream requestStream;
	static FileOutputStream responseStream;

//	static FastIPC server;
	protected String grammarName;
	protected String startRuleName;
	protected String fifoIn;
	protected String fifoOut;
	JSONObject json = null;
	Lexer lexer;
	Class<? extends Parser> parserClass;
	Constructor<? extends Lexer> lexerCtor;
	Parser parser;
	protected static final Logger logger=Logger.getLogger("MYLOG");

	public ParserIntf(String[] args) throws Exception {
		if ( args.length < 2 ) {
			System.err.println("java pyinterface.ParserIntf GrammarName startRuleName");
			System.out.println(Arrays.toString(args));
			return;
		}
		grammarName = args[0];
		startRuleName = args[1];
		fifoIn = args[2];
		fifoOut = args[3];

		requestStream = new  FileInputStream(fifoIn);
	    responseStream = new FileOutputStream(fifoOut);

		FileHandler fh = new FileHandler("/home/bvukobratovic/projects/pyde/parser_intf.log",true);
		fh.setFormatter(new SimpleFormatter());
        logger.addHandler(fh);
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

		lexerCtor = lexerClass.getConstructor(CharStream.class);

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
		logger.info("START SERVER");
//		int port = 32000;
//        server = new FastIPC(port);
//		out = new PrintWriter((new BufferedWriter(new FileWriter("pyde/out"))));
//		in = new PrintWriter((new BufferedWriter(new FileWriter("pyde/in"))));
        logger.info("Connected");
 		if(args.length >= 2) {
 			while(true) {
 				parserIntf.process();
 			}
		}
	}

	public void process() throws Exception {
//		System.out.println("exec "+grammarName+"."+startRuleName);

		StringBuilder inputText = new StringBuilder();
		int inp = requestStream.read();
		logger.info(Integer.toString(inp));
        while ((inp != -1) && (inp != 26))
		{
		    // converts integer to character
        	inputText.append((char)inp);
        	inp=requestStream.read();
//        	if (inp < 30) {
//        		logger.info(Integer.toString(inp));
//        	}
		}
        
//        while (text.isEmpty() || (text.charAt(0) != (char) 26)) {
//            inputText.append(text);
//            inputText.append("\n");
//            try {
//            	text = server.recv();
//            } catch (Exception msg) {
//				logger.info(msg.toString());
//			} 
//        }
        logger.info(inputText.toString());
//		byte[] inputEncoded = IOUtils.readFully(System.in, -1, true);
		long startTime = System.currentTimeMillis();
//		String inputText = new String(inputEncoded);
//		System.out.println("RECEIVED:");
//		System.out.print(inputText);
//		System.out.println("END_RECEIVED;");
		Reader r = new StringReader(inputText.toString());
//		Reader r = new StringReader("proba\n");
		lexer = lexerCtor.newInstance((CharStream)null);		
//        Reader r = new StringReader(inputText);
		System.out.format("Prepare the stream: %d\n", System.currentTimeMillis() - startTime);
		process(lexer, parserClass, parser, r);
	}
	
	protected void process(Lexer lexer, Class<? extends Parser> parserClass, Parser parser, Reader r) throws IOException, IllegalAccessException, InvocationTargetException, PrintException {
		try {
			long startTime = System.currentTimeMillis();
			ANTLRInputStream input = new ANTLRInputStream(r);
			lexer.setInputStream(input);
			CommonTokenStream tokens = new CommonTokenStream(lexer);

			tokens.fill();

			if ( startRuleName.equals(LEXER_START_RULE_NAME) ) return;
			
			parser.setBuildParseTree(true);

			parser.setTokenStream(tokens);
			
			System.out.format("Prepare the parser/lexer: %d\n", System.currentTimeMillis() - startTime);
			startTime = System.currentTimeMillis();
			try {
				startTime = System.currentTimeMillis();
				Method startRule = parserClass.getMethod(startRuleName);
				ParserRuleContext tree = (ParserRuleContext)startRule.invoke(parser, (Object[])null);
				System.out.format("Parse: %d\n", System.currentTimeMillis() - startTime);
				startTime = System.currentTimeMillis();
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
				
				System.out.format("Dump Tokens: %d\n", System.currentTimeMillis() - startTime);
//				parser.addParseListener(new AntlrParseListener(parser, jsTree));

				startTime = System.currentTimeMillis();
				AntlrParseListener listener = new AntlrParseListener(parser, jsTree);
				walker.walk(listener, tree); // initiate walk of tree with listener

				StringWriter out = new StringWriter();
				try {
					json.write(out);
				} catch (JSONException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				System.out.format("Dump Parse Tree: %d\n", System.currentTimeMillis() - startTime);
				startTime = System.currentTimeMillis();
				String text = out.toString();
				System.out.format("Serialize: %d\n", System.currentTimeMillis() - startTime);
				startTime = System.currentTimeMillis();
//				System.out.println(text);
				logger.info("RESPONSE:");
				//BufferedWriter log = new BufferedWriter(new OutputStreamWriter(System.out, "ASCII"), 256);
//				server.send(text);
				responseStream.write(text.getBytes());
				responseStream.write("\n".getBytes());
				responseStream.flush();
//                server.send("\n");
//                server.flush();

//				log.write(text);
//				log.write("\n");
//				log.flush();
				System.out.format("Send Results: %d\n", System.currentTimeMillis() - startTime);
				System.out.println();
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


