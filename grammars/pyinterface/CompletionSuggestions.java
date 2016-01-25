package pyinterface;

import java.io.File;
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

public class CompletionSuggestions {
	protected String grammarName;
	protected String startRuleName;
	protected String inputText = null;
	
	public CompletionSuggestions(String[] args) throws Exception {
	if ( args.length < 2 ) {
			System.err.println("java CompletionSuggestions GrammarName startRuleName\n" +
							   "  [text]");
			System.out.println(Arrays.toString(args));
			return;
		}
		int i=0;
		grammarName = args[i];
		i++;
		startRuleName = args[i];
		i++;
		inputText = args[i];
	}

	public static void main(String[] args) throws Exception {
		CompletionSuggestions c = new CompletionSuggestions(args);
 		if(args.length >= 2) {
			c.process();
		}
	}
	
	public void process() throws Exception {
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

		Constructor<? extends Lexer> lexerCtor = lexerClass.getConstructor(CharStream.class);
		Lexer lexer = lexerCtor.newInstance(new ANTLRInputStream(inputText));
		String lexerLocPath = lexer.getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
		
//		System.out.println(lexer.getGrammarFileName());
 		Grammar g = new Grammar(new String(Files.readAllBytes(Paths.get(lexerLocPath + '/' + this.grammarName + "/" + this.grammarName + ".g4"))));
		int startRuleIndex = g.getRule(startRuleName).index;
		
		CommonTokenStream tokens = new CommonTokenStream(lexer); 

		CompletionGrammarParserInterpreter parser = new CompletionGrammarParserInterpreter(g, tokens);
		tokens.fill();
		JSONArray s = parser.getSuggestions(g, startRuleIndex, tokens.size() - 2);
		System.out.println(s);

	}
}
