#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Instruction.h"
#include "llvm/Support/CommandLine.h"
#include <fstream>
#include <string>
#include <map>

using namespace llvm;
using namespace std;

#define DEBUG_TYPE "ValueNumbering"

using namespace llvm;

namespace {
  struct ValueNumbering : public FunctionPass {
      string func_name = "test";
      static char ID;
      map<Value*, int> VNMap;
      map<string, int> ExprMap;
      int vn = 1;

      ValueNumbering() : FunctionPass(ID) {}

      int addOrFindVN(Value* op,bool* found){
        auto temp = VNMap.find(op);
        int val = vn;

        if(temp != VNMap.end()){
          val = temp->second;
          *found = true;
        }
        else{
          VNMap.insert(make_pair(op, vn++));
          *found = false;
        }
        return val;
      }

      int addOrFindExpr(string expr,bool *found){
        auto temp = ExprMap.find(expr);
        int val = vn;

        if(temp != ExprMap.end()){
          val = temp->second;
          *found = true;
        }
        else{
          ExprMap.insert(make_pair(expr, vn++));
          *found = false;
        }
        return val;
      }

      bool runOnFunction(Function &F) override {
          errs() << "ValueNumbering: \n";
          errs() << "Function: " << F.getName() << "\n";
          string filename = F.getParent()->getSourceFileName();
          int lastindex = filename.find_last_of(".");
          string sourcefile = filename.substr(0, lastindex);
          string operation,expr;
          Value* dest;
          Value* operand1;
          Value* operand2;
          int valuenumber1,valuenumber2,valuenumber3;
          ofstream outfile;
         
          if (F.getName() != func_name) return false;

          for (auto& basic_block : F)
          {
            string outputfile = sourcefile + ".out";
            outfile.open(outputfile);
            for (auto& inst : basic_block)
            {
              errs() << " " << inst << "\n";
              if(inst.getOpcode() == Instruction::Load){
                      //errs() << "Load operation"<<"\n";
              }
              if(inst.getOpcode() == Instruction::Store){
                      //errs() << "Store operation"<<"\n";
              }
              if (inst.isBinaryOp())
              {
                  if(inst.getOpcode() == Instruction::Add){
                    operation = '+';
                  }
                  if(inst.getOpcode() == Instruction::Sub){
                    operation = '-';
                  }
                  if(inst.getOpcode() == Instruction::Mul){
                    operation = '*';
                  }
                  if(inst.getOpcode() == Instruction::SDiv || inst.getOpcode() == Instruction::UDiv){
                    operation = '/';
                  }

                  // Fetching the operands, as well as the destination.
                  auto* ptr = dyn_cast<User>(&inst);
                  Value* dest = dyn_cast<Value>(&inst);

                  int total_ops = ptr->getNumOperands();
                  if(total_ops == 1){
                    operand1 = ptr->getOperand(0);
                  }
                  if(total_ops == 2){
                    operand1 = ptr->getOperand(0);
                    operand2 = ptr->getOperand(1);
                  }
                 
                  bool *found = new bool(false);
                  valuenumber1 = addOrFindVN(operand1,found);
                  valuenumber2 = addOrFindVN(operand2,found);
                 
                  // Computing operations are handled in this block
                  if(valuenumber1 < valuenumber2){
                      expr = to_string(valuenumber1) + operation +  to_string(valuenumber2);
                  }
                  else{
                      expr = to_string(valuenumber2) + operation +  to_string(valuenumber1);
                  }
                  valuenumber3 = addOrFindExpr(expr,found);
                  if (*found){
                    errs() << "Redundant Expression: \n" << inst << "\n";
                    *found = false;
                  }
                  VNMap.insert(make_pair(dest, valuenumber3));
                  string output = to_string(valuenumber3) + "=" + to_string(valuenumber1) + operation +  to_string(valuenumber2);
                  outfile << output << "\n";
              }
            }
            outfile.close();
          }
          return false;
      }
  }; // end of struct ValueNumbering
}  // end of anonymous namespace

char ValueNumbering::ID = 0;
static RegisterPass<ValueNumbering> X("ValueNumbering", "ValueNumbering Pass",
                             false /* Only looks at CFG */,
                             false /* Analysis Pass */);


