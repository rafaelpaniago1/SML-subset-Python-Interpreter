# SML Subset Interpreter

Um interpretador para um subconjunto da linguagem SML (Standard ML) implementado em Python.

## 🚀 Características

Este interpretador suporta as seguintes funcionalidades da linguagem SML:

- **Tipos básicos**: Números inteiros e booleanos
- **Operações aritméticas**: `+`, `-`, `*`, `/`
- **Operações lógicas**: `and`, `or`, `not`
- **Comparações**: `=`, `<`, `<=`
- **Funções anônimas**: `fn x => expr`
- **Funções recursivas**: `fun nome x => expr`
- **Aplicação de funções**: `f x`
- **Expressões let**: `let x <- expr in expr end`
- **Condicionais**: `if cond then expr else expr`
- **Variáveis e closures**
- **Checagem de tipos estática**: Sistema de tipos com ArrowType para funções
- **Análise de uso/definição**: Detecção de variáveis não definidas

## 📋 Requisitos

- Python 3.6 ou superior
- Nenhuma dependência externa necessária

## 🛠️ Instalação

1. Clone ou baixe este repositório:
```bash
git clone https://github.com/rafaelpaniago1/SML-subset-Python-Interpreter.git
cd SML-subset-Python-Interpreter
```

2. Torne o script executável (opcional):
```bash
chmod +x sml.py
```

## 📖 Uso

### Modo básico
Execute um arquivo SML:
```bash
python3 sml.py programa.sml
```

### Entrada padrão
Leia código da entrada padrão:
```bash
echo "2 + 3 * 4" | python3 sml.py
```

### Modo interativo (REPL)
Inicie o modo interativo:
```bash
python3 sml.py -i
```

### Opções avançadas

- **Modo verboso** (mostra tokens e AST):
```bash
python3 sml.py -v programa.sml
```

- **Mostrar apenas tokens**:
```bash
python3 sml.py --tokens-only programa.sml
```

- **Mostrar apenas AST**:
```bash
python3 sml.py --ast-only programa.sml
```

- **Ajuda**:
```bash
python3 sml.py -h
```

## � Funções Recursivas

Este interpretador suporta **funções recursivas** usando a palavra-chave `fun`:

```sml
fun factorial n => 
  if n <= 1 then 1 
  else n * factorial (n - 1)

factorial 5  # => 120
```

```sml
fun fibonacci n =>
  if n <= 1 then n
  else fibonacci (n - 1) + fibonacci (n - 2)

fibonacci 7  # => 13
```

### Características das Funções Recursivas:
- **Sintaxe**: `fun nome parâmetro => corpo`
- **Escopo**: O nome da função está disponível dentro do corpo
- **Checagem de tipos**: Suporte completo a tipos de função (ArrowType)
- **Closures**: Acesso ao ambiente de definição

## 🔍 Sistema de Tipos

O interpretador inclui um **sistema de checagem de tipos estática**:

- **ArrowType**: Representa tipos de função `domínio -> codomínio`
- **Inferência de tipos**: Detecção automática de tipos
- **Detecção de erros**: Erros de tipo são detectados antes da execução
- **Unificação**: Sistema de unificação de tipos para expressões complexas

## �📝 Exemplos de Código

### Números e Operações Básicas
```sml
42
2 + 3 * 4
~5
```

### Booleanos e Lógica
```sml
true
false
not true
true and false
true or false
```

### Funções Anônimas
```sml
fn x => x + 1
(fn x => x * x) 5
```

### Funções Recursivas
```sml
fun power base exp =>
  if exp = 0 then 1
  else base * power base (exp - 1)

power 2 8  # => 256
```

### Funções de Ordem Superior
```sml
fn f => fn x => f (f x)
(fn x => fn y => x + y) 3 2

fun sum_range start finish =>
  if start > finish then 0
  else start + sum_range (start + 1) finish

sum_range 1 10  # => 55
```

### Let Expressions
```sml
let x <- 10 in x + 5 end
let f <- fn x => x * x in f 4 end
```

### Condicionais
```sml
if 2 < 3 then 100 else 200
let x <- 5 in if x > 0 then x else ~x end
```

### Exemplos Complexos

#### Função de Potenciação
```sml
let
  square <- fn x => x * x
in
  let
    twice <- fn f => fn x => f (f x)
  in
    (twice square) 3
  end
end
```

#### Closures e Escopo
```sml
let
  make_adder <- fn n => fn x => x + n
in
  let
    add5 <- make_adder 5
  in
    add5 10
  end
end
```

## 🎯 Modo Interativo

No modo interativo, você pode:

- Digite código SML linha por linha
- Use `:tokens` para ver os tokens da próxima expressão
- Use `:ast` para ver a AST da próxima expressão
- Use `help` para ver comandos disponíveis
- Use `quit` ou `exit` para sair

Exemplo de sessão:
```
$ python3 sml.py -i
SML Subset Interpreter - Modo Interativo
Digite 'quit' ou 'exit' para sair

sml> 2 + 3
=> 5

sml> fn x => x * x
=> Fn(x)

sml> (fn x => x * x) 4
=> 16

sml> let f <- fn x => x + 1 in f 5 end
=> 6

sml> quit
Goodbye!
```

## 🔧 Estrutura do Projeto

```
SML-subset-Python-Interpreter/
├── sml.py                    # Script principal
├── driver.py                 # Script original (para testes)
├── Expression.py             # Classes para AST (incluindo Fun para recursão)
├── Lexer.py                  # Analisador léxico
├── Parser.py                 # Analisador sintático
├── Visitor.py                # Padrão Visitor (EvalVisitor, TypeCheckVisitor, etc.)
├── Unifier.py                # Unificação de tipos
├── setup.py                  # Script de configuração
├── run_examples.py           # Executa todos os exemplos
├── requirements.txt          # Dependências
├── examples/                 # Exemplos de código SML
│   ├── basic.sml            # Operações básicas
│   ├── functions.sml        # Funções simples
│   ├── recursive.sml        # Funções recursivas simples
│   ├── advanced_recursive.sml # Funções recursivas avançadas
│   ├── conditionals.sml     # Estruturas condicionais
│   ├── let_expressions.sml  # Expressões let
│   └── complex.sml          # Exemplos complexos
├── USAGE.md                  # Guia de uso rápido
└── README.md                 # Este arquivo
```

## 🐛 Tratamento de Erros

O interpretador fornece mensagens de erro para:

- **Erros léxicos**: Caracteres não reconhecidos
- **Erros sintáticos**: Código malformado
- **Erros de tipo**: Operações inválidas
- **Variáveis indefinidas**: Uso de variáveis não declaradas
- **Arquivos não encontrados**: Caminhos inválidos

Exemplos de erros:
```bash
$ echo "2 +" | python3 sml.py
Erro: Parse error

$ echo "x" | python3 sml.py
Erro: Def error

$ echo "2 + true" | python3 sml.py
Erro: Type Error
```

## 🧪 Executando Testes

O projeto inclui o sistema de testes original:
```bash
# Teste manual de exemplos
python3 sml.py examples/basic.sml
python3 sml.py examples/functions.sml
```

## 📄 Licença

Este projeto está licenciado sob a licença especificada no arquivo `LICENSE`.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📞 Suporte

Se você encontrar bugs ou tiver sugestões:

1. Abra uma issue no GitHub
2. Descreva o problema ou sugestão detalhadamente
3. Inclua exemplos de código se aplicável

## 🎓 Sobre o Projeto

Este interpretador foi desenvolvido como parte de um projeto acadêmico para demonstrar:

- Implementação de um interpretador funcional
- Padrão Visitor para travessia de AST
- Análise léxica e sintática
- Avaliação de expressões funcionais
- Suporte a closures e escopo léxico

---

**Autor**: Rafael Paniago  
**Repositório**: https://github.com/rafaelpaniago1/SML-subset-Python-Interpreter
