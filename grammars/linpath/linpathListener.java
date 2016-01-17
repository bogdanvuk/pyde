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
	 * Enter a parse tree produced by {@link linpathParser#absolute_path}.
	 * @param ctx the parse tree
	 */
	void enterAbsolute_path(linpathParser.Absolute_pathContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#absolute_path}.
	 * @param ctx the parse tree
	 */
	void exitAbsolute_path(linpathParser.Absolute_pathContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#rel_path}.
	 * @param ctx the parse tree
	 */
	void enterRel_path(linpathParser.Rel_pathContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#rel_path}.
	 * @param ctx the parse tree
	 */
	void exitRel_path(linpathParser.Rel_pathContext ctx);
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