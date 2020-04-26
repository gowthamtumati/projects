#include "Liveness.h"
#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/ADT/StringMap.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/ADT/ilist_node.h"
#include "llvm/ADT/iterator_range.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Type.h"

#include <map>
#include <set>
#include <list>
#include <utility>
#include <algorithm>
#include <iterator>

#include <fstream>
#include <iostream>

using namespace llvm;
using namespace std;



namespace {
		// Here we begin, our Structure for the Liveness Analysis 
		struct Liveness : public FunctionPass {
				string func_name = "test";
				static char ID; 
				Liveness() : FunctionPass(ID) {}
				
				map<BasicBlock*, set<llvm::StringRef>> UpwardExposed; //setting up the map values for Upward Exposed Variables
				map<BasicBlock*, set<llvm::StringRef>> VariableKill; //setting up the map values for Variable Kill
				map<BasicBlock*, set<llvm::StringRef>>::iterator it;
				map<BasicBlock*, set<llvm::StringRef>>::iterator kit;

				map<BasicBlock*, set<llvm::StringRef>> LOut; //initializing the blocks for LiveOut computation block
				map<BasicBlock*, set<llvm::StringRef>>::iterator lit;
				std::list<BasicBlock*> workList;


				//This block is to create the output files that store the results at each BB
				ofstream createOutput(Function &F){  
						string filename = F.getParent() ->getSourceFileName();
						int index = filename.find_last_of(".");
						string sourcefile =filename.substr(0,index);
						ofstream pathOut;
						string outputfile = sourcefile + ".out";						
						pathOut.open(outputfile);
						return pathOut;
				}
			

				auto computeUpwardExposedandVarKill(Function &F,set<StringRef> UpwardExposedVariable, set<StringRef> VarKill, BasicBlock &BB ){


						for (Instruction &inst : BB) {
								//OpCode for load is 31, and UpwardExposedVariable is on the right side
								if (inst.getOpcode() == 31){
										StringRef var_name = inst.getOperand(0)->getName();
										kit = VariableKill.find(&BB);
										//var_name not in VariableKill
										if (kit->second.find(var_name) != kit->second.end()) continue;
										// put var_name into UpwardExposedVariable
										it = UpwardExposed.find(&BB);
										UpwardExposedVariable = it->second;
										UpwardExposedVariable.insert(var_name);
										UpwardExposed.erase(it);
										UpwardExposed.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(&BB,UpwardExposedVariable));
								}

								//OpCode used is 32 and VarKill is on the left side
								if (inst.getOpcode() == 32) {
										StringRef var_kill = inst.getOperand(1)->getName();
										// put var_kill into Varkill
										kit = VariableKill.find(&BB);
										VarKill = kit->second;
										VarKill.insert(var_kill);
										VariableKill.erase(kit);
										VariableKill.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(&BB,VarKill));
								}
						}
				}

				auto computeLOut(Function &F, map<BasicBlock*, set<llvm::StringRef>> UpwardExposed,
								map<BasicBlock*, set<llvm::StringRef>> VariableKill){

						for (BasicBlock &BB : F) {
								set<StringRef> LIVEOUT;
								LOut.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(&BB,LIVEOUT));
								workList.push_back(&BB);
						}
						while (!workList.empty()) {
								//BasicBlock Operation								
								BasicBlock* tmp = workList.front();
								workList.pop_front();
								map<BasicBlock*, set<llvm::StringRef>>::iterator it; 
								it = LOut.find(tmp);
								//Initial LiveOut								
								set<llvm::StringRef> originLIVEOUT = it->second;
								//LiveOut Computation
								const auto *TInst = tmp->getTerminator();
								set<llvm::StringRef> resultSet;//LIVEOUT result
								for (int i = 0, NSucc = TInst->getNumSuccessors(); i < NSucc; i++) {
										BasicBlock* succ = TInst->getSuccessor(i);// retrieve pointer for basicblock
										// retrieve successor's LIVEOUT,VARKILL,UpwardExposedVAR
										set<llvm::StringRef> LIVEOUT = LOut.find(succ)->second;
										set<llvm::StringRef> VarKill = VariableKill.find(succ)->second;
										set<llvm::StringRef> UpwardExposedVariable = UpwardExposed.find(succ)->second;
										set<llvm::StringRef> subtrSet (LIVEOUT);
										for (set<llvm::StringRef>::iterator setIt = VarKill.begin(); setIt != VarKill.end(); setIt++) {
												subtrSet.erase(*setIt);
										}
										std::set_union(UpwardExposedVariable.begin(), UpwardExposedVariable.end(), subtrSet.begin(),
														subtrSet.end(), std::inserter(resultSet, resultSet.begin()));
								}
								LOut.erase(it);// updation of LIVEOUT for current BB
								LOut.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(tmp,resultSet));
								if (resultSet != originLIVEOUT) {
										for (auto predIt = pred_begin(tmp), predEnd = pred_end(tmp); 
														predIt != predEnd; predIt++) {
												BasicBlock* pred = *predIt;
												workList.push_back(pred);
										}
								}
						}

				}

				auto printResult(Function &F, map<BasicBlock*, set<llvm::StringRef>> UpwardExposed,map<BasicBlock*, set<llvm::StringRef>> VariableKill, 
								map<BasicBlock*, set<llvm::StringRef>> LOut){


						//Creation of output file, to map the computations directly, at each step
						ofstream pathOut = createOutput(F);
						if (!pathOut.is_open()) 
								return 0;

						for (auto& BB : F){
								BasicBlock* key_BB = &BB;
								set<StringRef> VarKill = VariableKill.find(key_BB)->second;
								set<StringRef> UpwardExposedVariable = UpwardExposed.find(key_BB)->second;
								set<StringRef> LIVEOUT = LOut.find(key_BB)->second;
								errs() << "----- "<< key_BB->getName() << " -----\n";
								errs() << "UEVAR: ";

								string bb_name = key_BB->getName();
								pathOut<< "----- "<< bb_name << " -----\n";
								pathOut<<"UEVAR: ";
								string uevar;
								for (set<StringRef>::iterator it = UpwardExposedVariable.begin(); it != UpwardExposedVariable.end(); it++) {
										errs() << *it << " ";
										uevar = *it;
										pathOut<<uevar<<" ";
								}
								pathOut<<"\n";

								errs() << "\n";
								errs() << "VARKILL: ";
								pathOut<<"VARKILL: ";
								string varkill;

								for (set<StringRef>::iterator it = VarKill.begin(); it != VarKill.end(); it++) {
										errs() << *it << " ";
										varkill = *it;
										pathOut<<varkill<<" ";
								}
								pathOut<<"\n";

								errs() << "\n";
								errs() << "LIVEOUT: ";

								pathOut<<"LIVEOUT: ";
								string liveout;
								for (set<StringRef>::iterator it = LIVEOUT.begin(); it != LIVEOUT.end(); it++) {
										errs() << *it << " ";
										liveout = *it;
										pathOut<<liveout<<" ";
								}
								pathOut<<"\n";
								errs()<<"\n";
						}
						pathOut.close();
						return 0;

				}

				bool runOnFunction(Function &F) override {


						if (F.getName() != func_name) return false;

						for (BasicBlock &BB : F) {
								//initialize  UpwardExposedVariable and VarKill
								set<StringRef> UpwardExposedVariable;
								UpwardExposed.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(&BB,UpwardExposedVariable));
								set<StringRef> VarKill;
								VariableKill.insert(std::pair<BasicBlock*, std::set<llvm::StringRef>>(&BB,VarKill));

								computeUpwardExposedandVarKill(F, UpwardExposedVariable, VarKill, BB);

						}
						//Calculation of LiveOut for each block
						computeLOut(F, UpwardExposed, VariableKill);
						//Here, we display the output on the terminal, which consists of UpwardExposedVariable, VarKill, LiveOut for each block
						printResult(F, UpwardExposed, VariableKill, LOut);

						return false;
				}
		}; // Liveness Structure end
} // end of namespace

char Liveness::ID = 0;
static RegisterPass<Liveness> X("Liveness", "Liveness Analysis");
