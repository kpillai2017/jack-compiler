# Jack Compiler Documentation

Welcome to the comprehensive documentation for the Jack Compiler - a complete implementation of a compiler for the Jack language from the nand2tetris course.

## 📚 Documentation Files

### 1. **index.html** - Home & Overview
   - Project overview and features
   - What is Jack language
   - Quick navigation to all resources
   - **Start here!**

### 2. **getting-started.html** - Installation & Setup
   - System requirements
   - Step-by-step installation
   - Your first compilation
   - Command-line reference
   - Troubleshooting common setup issues

### 3. **how-it-works.html** - Deep Dive into Compiler Architecture
   - Understanding compilers (beginner-friendly)
   - The compilation pipeline (Lexer → Parser → Code Gen)
   - Introduction to ANTLR4
   - Visitor pattern explanation
   - Symbol table management
   - Design patterns used
   - Complete examples with code walkthrough
   - Error handling

### 4. **examples.html** - Real-World Code Samples
   - 5 complete examples:
     1. Hello World (string output)
     2. Variables and arithmetic
     3. Loops (while with accumulation)
     4. Object-oriented programming (classes, methods)
     5. Arrays (allocation and indexing)
   - Side-by-side Jack source and VM output
   - Key points explained for each example

### 5. **faq.html** - Frequently Asked Questions
   - General questions about the compiler
   - Installation troubleshooting
   - Common errors and solutions
   - Language features
   - Output compatibility
   - Learning resources

### 6. **jackvm.html** - Using the Compiler with JackVM
   - Setting up jack-compiler and jackvm-py side by side
   - Ctrl+J: run the compiled program in JackVM
   - Running .jack source from JackVM, and opening mistakes in the compiler
   - How each app finds the other (environment variable, same environment, PATH)
   - Troubleshooting

## 🚀 Quick Start

1. **Setup**: Read [getting-started.html](getting-started.html)
   ```bash
   git clone https://github.com/kpillai2017/jack-compiler.git
   cd jack-compiler
   pip install -e ".[dev]"
   ```

2. **Understand**: Read [how-it-works.html](how-it-works.html)
   - Learn how ANTLR4 works
   - Understand the compilation pipeline
   - See design patterns in action

3. **Learn by Example**: Check [examples.html](examples.html)
   - See real Jack code and its VM output
   - Understand translation patterns

4. **Reference**: Use [faq.html](faq.html) for answers to common questions

## 📖 Reading Recommendations

### For Complete Beginners:
1. Start with [index.html](index.html) for overview
2. Follow [getting-started.html](getting-started.html) to install
3. Read [how-it-works.html](how-it-works.html) "The Big Picture" section
4. Look at [examples.html](examples.html) Examples 1-2

### For Understanding the Architecture:
1. Read [how-it-works.html](how-it-works.html) completely
2. Study [examples.html](examples.html) Examples 3-5
3. Check [faq.html](faq.html) "Learning & Understanding" section

### For Reference:
1. [getting-started.html](getting-started.html) - Command-line usage
2. [faq.html](faq.html) - Common issues
3. [how-it-works.html](how-it-works.html) - Technical deep dives

## 🎯 Key Concepts Explained

### ANTLR4
A parser generator that automatically creates a parser from a grammar. Instead of writing a parser manually, you define the language rules and ANTLR4 generates the code.

### Visitor Pattern
A design pattern for traversing tree structures. The compiler uses it to walk through the parse tree and generate code.

### Symbol Table
A data structure that tracks all variables in the program - their names, types, kinds (local/field/static), and memory indices.

### Compilation Pipeline
1. **Lexer** - Tokenizes source code
2. **Parser** - Builds parse tree from tokens
3. **Visitor** - Traverses tree and builds symbol table
4. **Code Generator** - Emits VM instructions

## 📁 Project Structure

```
jack-compiler/
├── docs/                    # This documentation
│   ├── index.html          # Main documentation index
│   ├── getting-started.html
│   ├── how-it-works.html
│   ├── examples.html
│   ├── faq.html
│   └── README.md           # This file
├── grammar/                # ANTLR4 grammar
│   └── Jack.g4
├── jack_compiler/          # Python implementation
├── examples/               # Sample Jack programs
├── tests/                  # Test suite
└── pyproject.toml         # Package configuration (jackc CLI)
```

## 🔗 Related Resources

- **nand2tetris course**: https://www.nand2tetris.org/
- **jackvm-py** (companion Jack VM): https://github.com/kpillai2017/jackvm-py
- **ANTLR4 documentation**: https://www.antlr.org/
- **Jack Language Specification**: http://nand2tetris.org/chapters/chapter09.pdf

## ✨ Features of This Compiler

✅ Complete Jack language support  
✅ Single-pass O(n) compilation  
✅ ANTLR4-based parser generation  
✅ Full semantic analysis  
✅ Error detection and reporting  
✅ 100% compatible with nand2tetris tools  
✅ Batch compilation support  
✅ Well-documented and educational  

## 📝 License

Licensed for educational use in the nand2tetris course.

---

**Ready to get started?** Browse the docs online at
<https://kpillai2017.github.io/jack-compiler/>, or open [index.html](index.html)
locally and read [getting-started.html](getting-started.html) to begin!

These pages are published with GitHub Pages from the `docs/` folder of the
`main` branch, so changes merged to `main` go live automatically.
