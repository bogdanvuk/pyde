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
	 * Enter a parse tree produced by {@link linpathParser#relative_path}.
	 * @param ctx the parse tree
	 */
	void enterRelative_path(linpathParser.Relative_pathContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#relative_path}.
	 * @param ctx the parse tree
	 */
	void exitRelative_path(linpathParser.Relative_pathContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#step}.
	 * @param ctx the parse tree
	 */
	void enterStep(linpathParser.StepContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#step}.
	 * @param ctx the parse tree
	 */
	void exitStep(linpathParser.StepContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#abbreviatedStep}.
	 * @param ctx the parse tree
	 */
	void enterAbbreviatedStep(linpathParser.AbbreviatedStepContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#abbreviatedStep}.
	 * @param ctx the parse tree
	 */
	void exitAbbreviatedStep(linpathParser.AbbreviatedStepContext ctx);
	/**
	 * Enter a parse tree produced by {@link linpathParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void enterVariableReference(linpathParser.VariableReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link linpathParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void exitVariableReference(linpathParser.VariableReferenceContext ctx);
}