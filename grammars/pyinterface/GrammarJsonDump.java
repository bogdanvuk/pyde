package pyinterface;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;

import org.antlr.v4.tool.Grammar;
import org.json.JSONObject;

public class GrammarJsonDump {
	protected String grammarName;
	protected String outFile;
	
	public GrammarJsonDump(String[] args) throws Exception {
		if ( args.length < 2 ) {
			System.err.println("java GrammarJSONDump GrammarName OutFile\n");
			System.out.println(Arrays.toString(args));
			return;
		}
		int i=0;
		grammarName = args[i];
		i++;
		outFile = args[i];
	}

	public static void main(String[] args) throws Exception {
		GrammarJsonDump jsonDump = new GrammarJsonDump(args);
 		if(args.length >= 2) {
			jsonDump.process();
		}
	}
	
	public void process() throws Exception {
		System.out.println(System.getProperty("user.dir"));
		Grammar g = new Grammar(new String(Files.readAllBytes(Paths.get(this.grammarName + "/" + this.grammarName + ".g4"))));
		
		GrammarASTJson js = new GrammarASTJson(g);
		JSONObject rules = js.toJson();
		
		PrintWriter out = new PrintWriter(this.outFile);
		out.println(rules.toString());
		out.close();
	}

}
