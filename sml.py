#!/usr/bin/env python3
"""
SML Subset Interpreter
======================

Um interpretador para um subconjunto da linguagem SML (Standard ML).
Este interpretador suporta:
- Funções (fn x => expr)
- Expressões let-in-end
- Expressões condicionais (if-then-else)
- Operações aritméticas (+, -, *, /)
- Operações lógicas (and, or, not)
- Comparações (=, <, <=)
- Números inteiros e booleanos

Uso:
    python3 sml.py [opções] [arquivo]
    
Opções:
    -h, --help      Mostra esta mensagem de ajuda
    -i, --interactive  Modo interativo
    -v, --verbose   Modo verboso (mostra tokens e AST)
    --ast-only      Mostra apenas a AST sem avaliar
    --tokens-only   Mostra apenas os tokens
    
Se nenhum arquivo for especificado, lê da entrada padrão.
"""

import sys
import argparse
from Expression import *
from Visitor import *
from Lexer import Lexer
from Parser import Parser

def print_tokens(code):
    """Imprime os tokens gerados pelo lexer"""
    print("=== TOKENS ===")
    lexer = Lexer(code)
    tokens = list(lexer.tokens())
    for i, token in enumerate(tokens):
        print(f"{i:2d}: {token.text:10s} -> {token.kind}")
    print()
    return tokens

def print_ast(exp, indent=0):
    """Imprime a AST de forma hierárquica"""
    spaces = "  " * indent
    
    if isinstance(exp, Num):
        print(f"{spaces}Num({exp.num})")
    elif isinstance(exp, Bln):
        print(f"{spaces}Bln({exp.bln})")
    elif isinstance(exp, Var):
        print(f"{spaces}Var({exp.identifier})")
    elif isinstance(exp, Add):
        print(f"{spaces}Add")
        print_ast(exp.left, indent + 1)
        print_ast(exp.right, indent + 1)
    elif isinstance(exp, Sub):
        print(f"{spaces}Sub")
        print_ast(exp.left, indent + 1)
        print_ast(exp.right, indent + 1)
    elif isinstance(exp, Mul):
        print(f"{spaces}Mul")
        print_ast(exp.left, indent + 1)
        print_ast(exp.right, indent + 1)
    elif isinstance(exp, Div):
        print(f"{spaces}Div")
        print_ast(exp.left, indent + 1)
        print_ast(exp.right, indent + 1)
    elif isinstance(exp, Fn):
        print(f"{spaces}Fn({exp.formal.identifier})")
        print_ast(exp.body, indent + 1)
    elif isinstance(exp, App):
        print(f"{spaces}App")
        print(f"{spaces}  function:")
        print_ast(exp.function, indent + 2)
        print(f"{spaces}  argument:")
        print_ast(exp.actual, indent + 2)
    elif isinstance(exp, Let):
        print(f"{spaces}Let({exp.identifier.identifier})")
        print(f"{spaces}  value:")
        print_ast(exp.exp_def, indent + 2)
        print(f"{spaces}  body:")
        print_ast(exp.exp_body, indent + 2)
    elif isinstance(exp, IfThenElse):
        print(f"{spaces}IfThenElse")
        print(f"{spaces}  condition:")
        print_ast(exp.cond, indent + 2)
        print(f"{spaces}  then:")
        print_ast(exp.e0, indent + 2)
        print(f"{spaces}  else:")
        print_ast(exp.e1, indent + 2)
    else:
        print(f"{spaces}{type(exp).__name__}")

def evaluate_code(code, verbose=False):
    """Avalia um código SML e retorna o resultado"""
    try:
        lexer = Lexer(code)
        tokens = list(lexer.tokens())
        
        if verbose:
            print_tokens(code)
            
        parser = Parser(tokens)
        exp = parser.parse()
        
        if verbose:
            print("=== AST ===")
            print_ast(exp)
            print()
        
        visitor = EvalVisitor()
        result = exp.accept(visitor, {})
        
        return result, exp
        
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return None, None

def interactive_mode():
    """Modo interativo - REPL"""
    print("SML Subset Interpreter - Modo Interativo")
    print("Digite 'quit' ou 'exit' para sair")
    print("Digite 'help' para ver comandos disponíveis")
    print()
    
    while True:
        try:
            code = input("sml> ")
            
            if code.strip().lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif code.strip().lower() == 'help':
                print("""
Comandos disponíveis:
  help         - Mostra esta mensagem
  quit/exit    - Sai do interpretador
  :tokens      - Mostra os tokens da próxima expressão
  :ast         - Mostra a AST da próxima expressão
  
Exemplos de código SML:
  42
  true
  2 + 3 * 4
  fn x => x + 1
  (fn x => x * x) 5
  let x <- 10 in x + 5 end
  if 2 < 3 then "verdadeiro" else "falso"
                """)
                continue
            elif code.strip() == '':
                continue
            elif code.startswith(':tokens'):
                next_code = input("sml> ")
                print_tokens(next_code)
                continue
            elif code.startswith(':ast'):
                next_code = input("sml> ")
                try:
                    lexer = Lexer(next_code)
                    parser = Parser(list(lexer.tokens()))
                    exp = parser.parse()
                    print("=== AST ===")
                    print_ast(exp)
                except Exception as e:
                    print(f"Erro: {e}")
                continue
            
            result, exp = evaluate_code(code)
            if result is not None:
                print(f"=> {result}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def main():
    parser = argparse.ArgumentParser(
        description="Interpretador para um subconjunto da linguagem SML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 sml.py programa.sml        # Executa arquivo
  python3 sml.py -i                  # Modo interativo
  python3 sml.py -v programa.sml     # Modo verboso
  echo "2 + 3" | python3 sml.py     # Lê da entrada padrão
        """
    )
    
    parser.add_argument('arquivo', nargs='?', help='Arquivo SML para executar')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Modo interativo (REPL)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Modo verboso (mostra tokens e AST)')
    parser.add_argument('--ast-only', action='store_true',
                       help='Mostra apenas a AST sem avaliar')
    parser.add_argument('--tokens-only', action='store_true',
                       help='Mostra apenas os tokens')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    # Lê o código fonte
    if args.arquivo:
        try:
            with open(args.arquivo, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{args.arquivo}' não encontrado", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        code = sys.stdin.read()
    
    # Remove quebras de linha extras
    code = code.strip()
    
    if not code:
        print("Erro: Nenhum código fornecido", file=sys.stderr)
        sys.exit(1)
    
    try:
        lexer = Lexer(code)
        tokens = list(lexer.tokens())
        
        if args.tokens_only:
            print_tokens(code)
            return
            
        parser = Parser(tokens)
        exp = parser.parse()
        
        if args.ast_only:
            print("=== AST ===")
            print_ast(exp)
            return
        
        if args.verbose:
            print_tokens(code)
            print("=== AST ===")
            print_ast(exp)
            print()
            print("=== RESULTADO ===")
        
        visitor = EvalVisitor()
        result = exp.accept(visitor, {})
        print(result)
        
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()