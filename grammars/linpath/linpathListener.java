// Generated from linpath.g4 by ANTLR 4.5.1
package linpath;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link linpathParser}.
 */
public interface linpathListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link linpathParser#main}.
	 * @param ctx the parse tree
	 */
	void enterMain(linpathParser.MainContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#main}.
	 * @param ctx the parse tree
	 */
	void exitMain(linpathParser.MainContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#path}.
	 * @param ctx the parse tree
	 */
	void enterPath(linpathParser.PathContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#path}.
	 * @param ctx the parse tree
	 */
	void exitPath(linpathParser.PathContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#part}.
	 * @param ctx the parse tree
	 */
	void enterPart(linpathParser.PartContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#part}.
	 * @param ctx the parse tree
	 */
	void exitPart(linpathParser.PartContext ctx);
}