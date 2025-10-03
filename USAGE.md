# 🚀 Guia de Uso Rápido - SML Subset Interpreter

## Instalação e Configuração

1. **Clone o repositório** (ou baixe os arquivos):
```bash
git clone https://github.com/rafaelpaniago1/SML-subset-Python-Interpreter.git
cd SML-subset-Python-Interpreter
```

2. **Execute o script de configuração**:
```bash
python3 setup.py
```

## Como Executar Códigos SML

### 1. Modo Básico - Arquivo
```bash
# Crie um arquivo .sml
echo "2 + 3 * 4" > meu_programa.sml

# Execute o arquivo
python3 sml.py meu_programa.sml
```

### 2. Modo Básico - Entrada Padrão
```bash
# Execute código diretamente
echo "(fn x => x * x) 5" | python3 sml.py

# Ou digite código interativamente
python3 sml.py
# (digite seu código e pressione Ctrl+D)
```

### 3. Modo Interativo (REPL) - Recomendado para Iniciantes
```bash
python3 sml.py -i
```

No modo interativo você pode:
- Digitar código linha por linha
- Ver resultados instantaneamente  
- Usar comandos especiais como `:tokens` e `:ast`
- Digite `help` para ver todos os comandos
- Digite `quit` para sair

### 4. Executar Exemplos Prontos
```bash
# Execute um exemplo específico
python3 sml.py examples/basic.sml
python3 sml.py examples/functions.sml
python3 sml.py examples/complex.sml

# Execute todos os exemplos de uma vez
python3 run_examples.py
```

### 5. Modo Debug/Verboso
```bash
# Ver tokens e AST
python3 sml.py -v meu_programa.sml

# Ver apenas tokens
python3 sml.py --tokens-only meu_programa.sml

# Ver apenas AST
python3 sml.py --ast-only meu_programa.sml
```

## Exemplos de Código SML

### Básico
```sml
42                          # => 42
2 + 3 * 4                   # => 14
~5                          # => -5
true                        # => True
not false                   # => True
5 < 10                      # => True
```

### Funções Anônimas
```sml
fn x => x + 1                       # => Fn(x)
(fn x => x * x) 5                   # => 25
(fn x => fn y => x + y) 3 2         # => 5
```

### Funções Recursivas 🔥
```sml
fun factorial n => 
  if n <= 1 then 1 
  else n * factorial (n - 1)

factorial 5                         # => 120

fun fibonacci n =>
  if n <= 1 then n
  else fibonacci (n - 1) + fibonacci (n - 2)

fibonacci 8                         # => 21

fun power base exp =>
  if exp = 0 then 1
  else base * power base (exp - 1)

power 3 4                           # => 81
```

### Let Expressions
```sml
let x <- 10 in x + 5 end            # => 15
let f <- fn x => x * x in f 4 end   # => 16
```

### Condicionais
```sml
if 2 < 3 then 100 else 200          # => 100
if true then (fn x => x) else (fn y => y + 1)  # => Fn(x)
```

### Complexo (Closures, Funções de Ordem Superior e Recursão)
```sml
let
  sqr <- fn x => x * x
in
  let
    twice <- fn f => fn x => f (f x)
  in
    (twice sqr) 3
  end
end                                  # => 81

fun sum_range start finish =>
  if start > finish then 0
  else start + sum_range (start + 1) finish

sum_range 1 10                       # => 55

# Combinando let e fun
let
  factorial <- fun fact n =>
    if n <= 1 then 1
    else n * fact (n - 1)
in
  factorial 6
end                                  # => 720
```

## Estrutura de Arquivos

```
SML-subset-Python-Interpreter/
├── sml.py              # 🔥 SCRIPT PRINCIPAL - Use este!
├── setup.py            # Script de configuração
├── run_examples.py     # Executa todos os exemplos
├── requirements.txt    # Dependências (só Python padrão)
├── README.md           # Documentação completa
├── examples/           # Exemplos de código SML
│   ├── basic.sml      # Operações básicas
│   ├── functions.sml  # Funções anônimas
│   ├── recursive.sml  # 🔥 Funções recursivas simples
│   ├── advanced_recursive.sml # 🔥 Funções recursivas avançadas
│   ├── conditionals.sml # Condicionais
│   ├── let_expressions.sml # Let expressions
│   └── complex.sml    # Exemplos avançados
├── USAGE.md           # Este guia
└── driver.py          # Script original (para testes acadêmicos)
```

## Comandos Essenciais

| Comando | Descrição |
|---------|-----------|
| `python3 sml.py -i` | Modo interativo (melhor para começar) |
| `python3 sml.py arquivo.sml` | Executar arquivo |
| `echo "código" \| python3 sml.py` | Executar código direto |
| `python3 sml.py -h` | Ajuda completa |
| `python3 setup.py` | Configurar/testar instalação |
| `python3 run_examples.py` | Executar todos os exemplos |

## Dicas de Uso

1. **Para iniciantes**: Comece com `python3 sml.py -i` (modo interativo)
2. **Para debug**: Use `python3 sml.py -v arquivo.sml` (modo verboso)
3. **Para aprender**: Execute `python3 run_examples.py` para ver vários exemplos
4. **Para desenvolver**: Crie arquivos `.sml` e execute com `python3 sml.py arquivo.sml`
5. **🔥 Para funções recursivas**: Use `fun nome parâmetro => corpo` em vez de `fn`
6. **Para checagem de tipos**: O sistema detecta automaticamente erros de tipo
7. **Para funções complexas**: Combine `let`, `fun` e closures para algoritmos avançados

## Solução de Problemas

- **"comando não encontrado"**: Use `python3` em vez de `python`
- **"arquivo não encontrado"**: Verifique se está na pasta correta
- **"parse error"**: Verifique a sintaxe do código SML
- **"def error"**: Variável não definida
- **Para mais ajuda**: Execute `python3 setup.py` para verificar a instalação

---

🎯 **Dica**: Comece experimentando no modo interativo (`python3 sml.py -i`) - é mais fácil para aprender!