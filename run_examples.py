#!/usr/bin/env python3
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
        print(f"\n📁 Executando {sml_file}:")
        print("-" * 30)
        
        try:
            # Lê o conteúdo do arquivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Executa cada linha não-comentário
            lines = [line.strip() for line in content.split('\n') 
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
