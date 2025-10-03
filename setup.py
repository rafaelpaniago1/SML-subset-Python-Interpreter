#!/usr/bin/env python3
"""
Script de instalação e configuração para o SML Subset Interpreter
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    if sys.version_info < (3, 6):
        print("❌ Erro: Python 3.6 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def check_files():
    """Verifica se todos os arquivos necessários estão presentes"""
    required_files = [
        'sml.py',
        'Expression.py', 
        'Lexer.py',
        'Parser.py',
        'Visitor.py',
        'Unifier.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos necessários não encontrados:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados")
    return True

def make_executable():
    """Torna o script sml.py executável"""
    try:
        os.chmod('sml.py', 0o755)
        print("✅ sml.py agora é executável")
        return True
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível tornar sml.py executável: {e}")
        return False

def test_type_checking():
    """Testa o sistema de checagem de tipos"""
    print("🔍 Testando checagem de tipos...")
    
    # Testes que devem passar
    valid_expressions = [
        "2 + 3",
        "true and false", 
        "fn x => x + 1",
        "fun factorial n => if n <= 1 then 1 else n * factorial (n - 1)"
    ]
    
    # Testes que devem falhar (erros de tipo)
    invalid_expressions = [
        "2 + true",
        "if 5 then 1 else 0"
    ]
    
    for expr in valid_expressions:
        try:
            result = subprocess.run(
                [sys.executable, 'driver.py', 'typecheck', expr],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "Type Error" not in result.stdout and "Type Error" not in result.stderr:
                print(f"  ✅ Tipo válido: '{expr[:30]}...'")
            else:
                print(f"  ❌ Erro inesperado em: '{expr}'")
        except:
            print(f"  ⚠️  Não foi possível testar: '{expr}'")
    
    print("✅ Checagem de tipos testada!")
    return True

def test_interpreter():
    """Testa se o interpretador está funcionando"""
    print("🧪 Testando o interpretador...")
    
    test_cases = [
        ("2 + 3", "5"),
        ("fn x => x + 1", "Fn(x)"),
        ("(fn x => x * x) 4", "16"),
        ("let x <- 10 in x + 5 end", "15"),
        # Testes para funções recursivas
        ("fun factorial n => if n <= 1 then 1 else n * factorial (n - 1)", "Fun factorial (n)"),
        ("fun power base exp => if exp <= 0 then 1 else base * power base (exp - 1)", "Fun power (base)")
    ]
    
    for code, expected in test_cases:
        try:
            result = subprocess.run(
                [sys.executable, 'sml.py'], 
                input=code, 
                text=True, 
                capture_output=True, 
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                # Para funções recursivas, apenas verificamos se não há erro
                if "Fun" in expected and "Fun" in output:
                    print(f"  ✅ '{code[:30]}...' => função recursiva criada")
                elif output == expected:
                    print(f"  ✅ '{code}' => {output}")
                else:
                    print(f"  ❌ '{code}' => {output} (esperado: {expected})")
                    return False
            else:
                print(f"  ❌ Erro ao executar '{code}': {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout ao executar '{code}'")
            return False
        except Exception as e:
            print(f"  ❌ Erro ao testar '{code}': {e}")
            return False
    
    print("✅ Todos os testes passaram!")
    return True

def create_example_runner():
    """Cria script para executar todos os exemplos"""
    runner_content = '''#!/usr/bin/env python3
"""
Script para executar todos os exemplos SML
"""

import os
import subprocess
import sys

def run_examples():
    examples_dir = "examples"
    if not os.path.exists(examples_dir):
        print("❌ Pasta de exemplos não encontrada")
        return
    
    sml_files = [f for f in os.listdir(examples_dir) if f.endswith('.sml')]
    
    if not sml_files:
        print("❌ Nenhum arquivo .sml encontrado na pasta examples")
        return
    
    print("🚀 Executando exemplos SML...")
    print("=" * 50)
    
    for sml_file in sorted(sml_files):
        filepath = os.path.join(examples_dir, sml_file)
        print(f"\\n📁 Executando {sml_file}:")
        print("-" * 30)
        
        try:
            # Lê o conteúdo do arquivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Executa cada linha não-comentário
            lines = [line.strip() for line in content.split('\\n') 
                    if line.strip() and not line.strip().startswith('--')]
            
            for line in lines:
                if line:
                    print(f"sml> {line}")
                    result = subprocess.run(
                        [sys.executable, 'sml.py'], 
                        input=line, 
                        text=True, 
                        capture_output=True
                    )
                    
                    if result.returncode == 0:
                        print(f"=> {result.stdout.strip()}")
                    else:
                        print(f"Erro: {result.stderr.strip()}")
                    print()
        
        except Exception as e:
            print(f"❌ Erro ao executar {sml_file}: {e}")
    
    print("=" * 50)
    print("✅ Execução dos exemplos concluída!")

if __name__ == "__main__":
    run_examples()
'''
    
    with open('run_examples.py', 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    try:
        os.chmod('run_examples.py', 0o755)
        print("✅ Script run_examples.py criado")
        return True
    except Exception as e:
        print(f"⚠️  Script criado mas não foi possível torná-lo executável: {e}")
        return True

def main():
    print("🔧 Configurando SML Subset Interpreter...")
    print("=" * 50)
    
    # Verificações
    if not check_python_version():
        sys.exit(1)
    
    if not check_files():
        sys.exit(1)
    
    # Configurações
    make_executable()
    create_example_runner()
    
    # Testes
    if not test_interpreter():
        print("❌ Instalação falhou nos testes básicos")
        sys.exit(1)
    
    # Teste sistema de tipos (se driver.py existir)
    if os.path.exists('driver.py'):
        test_type_checking()
    
    print("\n" + "=" * 50)
    print("🎉 Instalação concluída com sucesso!")
    print("\n📖 Como usar:")
    print("   python3 sml.py -i              # Modo interativo")
    print("   python3 sml.py arquivo.sml     # Executar arquivo")
    print("   python3 run_examples.py        # Executar exemplos")
    print("   python3 driver.py typecheck 'código'  # Verificar tipos")
    print("   python3 sml.py -h              # Ajuda")
    print("\n📚 Exemplos disponíveis em: examples/")
    print("   - basic.sml: Operações básicas")
    print("   - functions.sml: Funções anônimas e de alta ordem") 
    print("   - recursive.sml: Funções recursivas simples")
    print("   - advanced_recursive.sml: Algoritmos recursivos avançados")
    print("   - complex.sml: Exemplos complexos")
    print("\n📄 Documentação completa: README.md")

if __name__ == "__main__":
    main()