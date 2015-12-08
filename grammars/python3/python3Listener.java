// Generated from python3.g4 by ANTLR 4.5.1
package python3;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link python3Parser}.
 */
public interface python3Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link python3Parser#single_input}.
	 * @param ctx the parse tree
	 */
	void enterSingle_input(python3Parser.Single_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#single_input}.
	 * @param ctx the parse tree
	 */
	void exitSingle_input(python3Parser.Single_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#file_input}.
	 * @param ctx the parse tree
	 */
	void enterFile_input(python3Parser.File_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#file_input}.
	 * @param ctx the parse tree
	 */
	void exitFile_input(python3Parser.File_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#eval_input}.
	 * @param ctx the parse tree
	 */
	void enterEval_input(python3Parser.Eval_inputContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#eval_input}.
	 * @param ctx the parse tree
	 */
	void exitEval_input(python3Parser.Eval_inputContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void enterDecorator(python3Parser.DecoratorContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void exitDecorator(python3Parser.DecoratorContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void enterDecorators(python3Parser.DecoratorsContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void exitDecorators(python3Parser.DecoratorsContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void enterDecorated(python3Parser.DecoratedContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void exitDecorated(python3Parser.DecoratedContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void enterFuncdef(python3Parser.FuncdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void exitFuncdef(python3Parser.FuncdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void enterParameters(python3Parser.ParametersContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void exitParameters(python3Parser.ParametersContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void enterTypedargslist(python3Parser.TypedargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void exitTypedargslist(python3Parser.TypedargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void enterTfpdef(python3Parser.TfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void exitTfpdef(python3Parser.TfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void enterVarargslist(python3Parser.VarargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void exitVarargslist(python3Parser.VarargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void enterVfpdef(python3Parser.VfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void exitVfpdef(python3Parser.VfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(python3Parser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(python3Parser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSimple_stmt(python3Parser.Simple_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSimple_stmt(python3Parser.Simple_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSmall_stmt(python3Parser.Small_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#small_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSmall_stmt(python3Parser.Small_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void enterExpr_stmt(python3Parser.Expr_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#expr_stmt}.
	 * @param ctx the parse tree
	 */
	void exitExpr_stmt(python3Parser.Expr_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#testlist_star_expr}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_star_expr(python3Parser.Testlist_star_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#testlist_star_expr}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_star_expr(python3Parser.Testlist_star_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void enterAugassign(python3Parser.AugassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void exitAugassign(python3Parser.AugassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void enterDel_stmt(python3Parser.Del_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#del_stmt}.
	 * @param ctx the parse tree
	 */
	void exitDel_stmt(python3Parser.Del_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void enterPass_stmt(python3Parser.Pass_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#pass_stmt}.
	 * @param ctx the parse tree
	 */
	void exitPass_stmt(python3Parser.Pass_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFlow_stmt(python3Parser.Flow_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#flow_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFlow_stmt(python3Parser.Flow_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void enterBreak_stmt(python3Parser.Break_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void exitBreak_stmt(python3Parser.Break_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void enterContinue_stmt(python3Parser.Continue_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void exitContinue_stmt(python3Parser.Continue_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void enterReturn_stmt(python3Parser.Return_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void exitReturn_stmt(python3Parser.Return_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void enterYield_stmt(python3Parser.Yield_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#yield_stmt}.
	 * @param ctx the parse tree
	 */
	void exitYield_stmt(python3Parser.Yield_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void enterRaise_stmt(python3Parser.Raise_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#raise_stmt}.
	 * @param ctx the parse tree
	 */
	void exitRaise_stmt(python3Parser.Raise_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(python3Parser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(python3Parser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#import_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_name(python3Parser.Import_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#import_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_name(python3Parser.Import_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#import_from}.
	 * @param ctx the parse tree
	 */
	void enterImport_from(python3Parser.Import_fromContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#import_from}.
	 * @param ctx the parse tree
	 */
	void exitImport_from(python3Parser.Import_fromContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_name(python3Parser.Import_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#import_as_name}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_name(python3Parser.Import_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_name(python3Parser.Dotted_as_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#dotted_as_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_name(python3Parser.Dotted_as_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void enterImport_as_names(python3Parser.Import_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#import_as_names}.
	 * @param ctx the parse tree
	 */
	void exitImport_as_names(python3Parser.Import_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void enterDotted_as_names(python3Parser.Dotted_as_namesContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#dotted_as_names}.
	 * @param ctx the parse tree
	 */
	void exitDotted_as_names(python3Parser.Dotted_as_namesContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void enterDotted_name(python3Parser.Dotted_nameContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#dotted_name}.
	 * @param ctx the parse tree
	 */
	void exitDotted_name(python3Parser.Dotted_nameContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void enterGlobal_stmt(python3Parser.Global_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#global_stmt}.
	 * @param ctx the parse tree
	 */
	void exitGlobal_stmt(python3Parser.Global_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#nonlocal_stmt}.
	 * @param ctx the parse tree
	 */
	void enterNonlocal_stmt(python3Parser.Nonlocal_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#nonlocal_stmt}.
	 * @param ctx the parse tree
	 */
	void exitNonlocal_stmt(python3Parser.Nonlocal_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void enterAssert_stmt(python3Parser.Assert_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#assert_stmt}.
	 * @param ctx the parse tree
	 */
	void exitAssert_stmt(python3Parser.Assert_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void enterCompound_stmt(python3Parser.Compound_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void exitCompound_stmt(python3Parser.Compound_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void enterIf_stmt(python3Parser.If_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void exitIf_stmt(python3Parser.If_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWhile_stmt(python3Parser.While_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWhile_stmt(python3Parser.While_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFor_stmt(python3Parser.For_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFor_stmt(python3Parser.For_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void enterTry_stmt(python3Parser.Try_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#try_stmt}.
	 * @param ctx the parse tree
	 */
	void exitTry_stmt(python3Parser.Try_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWith_stmt(python3Parser.With_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#with_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWith_stmt(python3Parser.With_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#with_item}.
	 * @param ctx the parse tree
	 */
	void enterWith_item(python3Parser.With_itemContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#with_item}.
	 * @param ctx the parse tree
	 */
	void exitWith_item(python3Parser.With_itemContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#except_clause}.
	 * @param ctx the parse tree
	 */
	void enterExcept_clause(python3Parser.Except_clauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#except_clause}.
	 * @param ctx the parse tree
	 */
	void exitExcept_clause(python3Parser.Except_clauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#suite}.
	 * @param ctx the parse tree
	 */
	void enterSuite(python3Parser.SuiteContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#suite}.
	 * @param ctx the parse tree
	 */
	void exitSuite(python3Parser.SuiteContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#test}.
	 * @param ctx the parse tree
	 */
	void enterTest(python3Parser.TestContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#test}.
	 * @param ctx the parse tree
	 */
	void exitTest(python3Parser.TestContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#test_nocond}.
	 * @param ctx the parse tree
	 */
	void enterTest_nocond(python3Parser.Test_nocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#test_nocond}.
	 * @param ctx the parse tree
	 */
	void exitTest_nocond(python3Parser.Test_nocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void enterLambdef(python3Parser.LambdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void exitLambdef(python3Parser.LambdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#lambdef_nocond}.
	 * @param ctx the parse tree
	 */
	void enterLambdef_nocond(python3Parser.Lambdef_nocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#lambdef_nocond}.
	 * @param ctx the parse tree
	 */
	void exitLambdef_nocond(python3Parser.Lambdef_nocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#or_test}.
	 * @param ctx the parse tree
	 */
	void enterOr_test(python3Parser.Or_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#or_test}.
	 * @param ctx the parse tree
	 */
	void exitOr_test(python3Parser.Or_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#and_test}.
	 * @param ctx the parse tree
	 */
	void enterAnd_test(python3Parser.And_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#and_test}.
	 * @param ctx the parse tree
	 */
	void exitAnd_test(python3Parser.And_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#not_test}.
	 * @param ctx the parse tree
	 */
	void enterNot_test(python3Parser.Not_testContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#not_test}.
	 * @param ctx the parse tree
	 */
	void exitNot_test(python3Parser.Not_testContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(python3Parser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(python3Parser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#comp_op}.
	 * @param ctx the parse tree
	 */
	void enterComp_op(python3Parser.Comp_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#comp_op}.
	 * @param ctx the parse tree
	 */
	void exitComp_op(python3Parser.Comp_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#star_expr}.
	 * @param ctx the parse tree
	 */
	void enterStar_expr(python3Parser.Star_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#star_expr}.
	 * @param ctx the parse tree
	 */
	void exitStar_expr(python3Parser.Star_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(python3Parser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(python3Parser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#and_expr}.
	 * @param ctx the parse tree
	 */
	void enterAnd_expr(python3Parser.And_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#and_expr}.
	 * @param ctx the parse tree
	 */
	void exitAnd_expr(python3Parser.And_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void enterShift_expr(python3Parser.Shift_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#shift_expr}.
	 * @param ctx the parse tree
	 */
	void exitShift_expr(python3Parser.Shift_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void enterArith_expr(python3Parser.Arith_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#arith_expr}.
	 * @param ctx the parse tree
	 */
	void exitArith_expr(python3Parser.Arith_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(python3Parser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(python3Parser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(python3Parser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(python3Parser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#power}.
	 * @param ctx the parse tree
	 */
	void enterPower(python3Parser.PowerContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#power}.
	 * @param ctx the parse tree
	 */
	void exitPower(python3Parser.PowerContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#atom_group}.
	 * @param ctx the parse tree
	 */
	void enterAtom_group(python3Parser.Atom_groupContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#atom_group}.
	 * @param ctx the parse tree
	 */
	void exitAtom_group(python3Parser.Atom_groupContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(python3Parser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(python3Parser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void enterTestlist_comp(python3Parser.Testlist_compContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#testlist_comp}.
	 * @param ctx the parse tree
	 */
	void exitTestlist_comp(python3Parser.Testlist_compContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void enterTrailer(python3Parser.TrailerContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void exitTrailer(python3Parser.TrailerContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void enterSubscriptlist(python3Parser.SubscriptlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void exitSubscriptlist(python3Parser.SubscriptlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void enterSubscript(python3Parser.SubscriptContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void exitSubscript(python3Parser.SubscriptContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void enterSliceop(python3Parser.SliceopContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void exitSliceop(python3Parser.SliceopContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void enterExprlist(python3Parser.ExprlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void exitExprlist(python3Parser.ExprlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void enterTestlist(python3Parser.TestlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void exitTestlist(python3Parser.TestlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void enterDictorsetmaker(python3Parser.DictorsetmakerContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void exitDictorsetmaker(python3Parser.DictorsetmakerContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void enterClassdef(python3Parser.ClassdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void exitClassdef(python3Parser.ClassdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void enterArglist(python3Parser.ArglistContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void exitArglist(python3Parser.ArglistContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#argument}.
	 * @param ctx the parse tree
	 */
	void enterArgument(python3Parser.ArgumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#argument}.
	 * @param ctx the parse tree
	 */
	void exitArgument(python3Parser.ArgumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void enterComp_iter(python3Parser.Comp_iterContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#comp_iter}.
	 * @param ctx the parse tree
	 */
	void exitComp_iter(python3Parser.Comp_iterContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#comp_for}.
	 * @param ctx the parse tree
	 */
	void enterComp_for(python3Parser.Comp_forContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#comp_for}.
	 * @param ctx the parse tree
	 */
	void exitComp_for(python3Parser.Comp_forContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#comp_if}.
	 * @param ctx the parse tree
	 */
	void enterComp_if(python3Parser.Comp_ifContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#comp_if}.
	 * @param ctx the parse tree
	 */
	void exitComp_if(python3Parser.Comp_ifContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void enterYield_expr(python3Parser.Yield_exprContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#yield_expr}.
	 * @param ctx the parse tree
	 */
	void exitYield_expr(python3Parser.Yield_exprContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#yield_arg}.
	 * @param ctx the parse tree
	 */
	void enterYield_arg(python3Parser.Yield_argContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#yield_arg}.
	 * @param ctx the parse tree
	 */
	void exitYield_arg(python3Parser.Yield_argContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#string}.
	 * @param ctx the parse tree
	 */
	void enterString(python3Parser.StringContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#string}.
	 * @param ctx the parse tree
	 */
	void exitString(python3Parser.StringContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(python3Parser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(python3Parser.NumberContext ctx);
	/**
	 * Enter a parse tree produced by {@link python3Parser#integer}.
	 * @param ctx the parse tree
	 */
	void enterInteger(python3Parser.IntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link python3Parser#integer}.
	 * @param ctx the parse tree
	 */
	void exitInteger(python3Parser.IntegerContext ctx);
}