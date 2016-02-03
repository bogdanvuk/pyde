package pyinterface;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.Reader;
import java.io.StringReader;
import java.io.StringWriter;
import java.lang.reflect.Constructor;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.tool.Grammar;
import org.json.JSONArray;
import org.json.JSONException;

public class CompletionSuggestions {
	protected String grammarName;
	protected String startRuleName;
	protected String inputText = null;
	static FileInputStream requestStream;
	static FileOutputStream responseStream;
	protected String fifoIn = null;
	protected String fifoOut = null;
	Constructor<? extends Lexer> lexerCtor;
	Grammar g;
	int startRuleIndex;
	
	public CompletionSuggestions(String[] args) throws Exception {
	if ( args.length < 2 ) {
			System.err.println("java CompletionSuggestions GrammarName startRuleName\n" +
							   "  [text]");
			System.out.println(Arrays.toString(args));
			return;
		}

		grammarName = args[0];
		startRuleName = args[1];
		if(args.length == 3) {
			inputText = args[2];
		} else {
			fifoIn = args[2];
			fifoOut = args[3];
		}
		
		if (fifoIn != null) {
				requestStream = new  FileInputStream(fifoIn);
			    responseStream = new FileOutputStream(fifoOut);
		}
		
		String lexerName = grammarName + "." + grammarName+"Lexer";
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
		String lexerLocPath = lexerClass.getProtectionDomain().getCodeSource().getLocation().getPath();
		g = new Grammar(new String(Files.readAllBytes(Paths.get(lexerLocPath + '/' + this.grammarName + "/" + this.grammarName + ".g4"))));
		startRuleIndex = g.getRule(startRuleName).index;
	}

	public static void main(String[] args) throws Exception {
		CompletionSuggestions c = new CompletionSuggestions(args);
		if (c.fifoIn != null) {
			c.pipeConnection();
		} else {
	        Reader r = new StringReader(c.inputText.toString());
			JSONArray s = c.process(r);
			System.out.println(s.toString());
		}
	}
	
	public void pipeConnection() throws Exception {
		while(true) {
			StringBuilder inputText = new StringBuilder();
			int inp = requestStream.read();
	        while ((inp != -1) && (inp != 26))
			{
	        	inputText.append((char)inp);
	        	inp=requestStream.read();
			}
	        Reader r = new StringReader(inputText.toString());
			JSONArray s = process(r);
			
			responseStream.write(s.toString().getBytes());
			responseStream.write("\n".getBytes());
			responseStream.flush();

		}
	}
	
	public JSONArray process(Reader r) throws Exception {
		Lexer lexer = lexerCtor.newInstance(new ANTLRInputStream(r));
	
		CommonTokenStream tokens = new CommonTokenStream(lexer); 

		CompletionGrammarParserInterpreter parser = new CompletionGrammarParserInterpreter(g, tokens);
		tokens.fill();
		JSONArray suggestions = new JSONArray();
		parser.getSuggestions(g, suggestions, startRuleIndex, tokens.size()-2);
		return suggestions;
//		for (int i = 0; i < s_next .length(); i++) {
//			s_cur.put(s_next.getJSONObject(i));
//		}
//		return s_cur;
	}
}
