# Reference Compiler Compatibility Guide

## Status: In Progress

This document tracks adjustments to ensure our ANTLR4-based Jack compiler produces output compatible with the reference implementation in `~/WorkData/Dev/web-ide`.

## Adjustments Made

### 1. ✅ Grammar Updated
- **File**: `grammar/Jack.g4`
- **Change**: Added `char` type support
- **Status**: COMPLETE
- **Details**:
  - Added `CHAR` keyword to type rules
  - Added `CHAR : 'char';` to lexer
  - Now supports: `int`, `char`, `boolean`, `String`, and custom classes

### 2. 🔄 AST Structure Update (In Progress)
- **File**: `src/compiler_visitor.py`
- **Change**: Update to match reference AST format
- **Status**: PENDING
- **Details**:
  - Reference uses: `nodeType`, `termType`, `statementType` fields
  - Must include `span` information for all nodes
  - Expression structure: `{ nodeType: "expression", term: {...}, rest: [...] }`
  - Term types: `numericLiteral`, `stringLiteral`, `keywordLiteral`, `variable`, `arrayAccess`, `subroutineCall`, `groupedExpression`, `unaryExpression`

### 3. 🔄 VM Code Generator Update (Pending)
- **File**: `src/codegen.py`
- **Change**: Format VM output with proper indentation
- **Status**: PENDING
- **Details**:
  - Indent all instructions with 4 spaces
  - Proper function declaration format
  - Correct stack operation order

## Reference Implementation Structure

### Location
```
/Users/kpillai/WorkData/Dev/web-ide/simulator/src/languages/
├── grammars/jack.ohm      (OHM grammar)
├── jack.ts                (Parser + AST generation)
└── jack.test.ts           (Tests)
```

### Key AST Patterns

#### Class Node
```typescript
{
  name: { value: string; span: Span };
  varDecs: ClassVarDec[];
  subroutines: Subroutine[];
}
```

#### Subroutine Node
```typescript
{
  type: "constructor" | "function" | "method";
  name: { value: string; span: Span };
  returnType: { value: ReturnType; span: Span };
  parameters: Parameter[];
  body: SubroutineBody;
}
```

#### Expression Node (Reference Format)
```typescript
{
  nodeType: "expression";
  term: Term;
  rest: {
    op: Op;
    term: Term;
  }[];
}
```

#### Term Node (Reference Format)
```typescript
// Numeric Literal
{ termType: "numericLiteral"; value: number }

// String Literal
{ termType: "stringLiteral"; value: string }

// Keyword Constant
{ termType: "keywordLiteral"; value: KeywordConstant }

// Variable
{ termType: "variable"; name: string; span: Span }

// Array Access
{ termType: "arrayAccess"; name: Identifier; index: Expression; span: Span }

// Subroutine Call
{ termType: "subroutineCall"; name: Identifier; parameters: Expression[]; span: Span }

// Grouped Expression
{ termType: "groupedExpression"; expression: Expression }

// Unary Expression
{ termType: "unaryExpression"; op: UnaryOp; term: Term }
```

## Expected VM Output Format

Reference generates:
```
function ClassName.methodName numLocals
    push constant 1
    push constant 2
    add
    call Output.printInt 1
    pop temp 0
    push constant 0
    return
```

Format requirements:
1. `function` keyword followed by function name and local variable count
2. All instructions indented with 4 spaces
3. Proper stack operations in correct order
4. Function calls with argument count
5. Return statements at end

## Example: Seven.jack

### Input
```jack
class Main {
    function void main() {
        do Output.printInt(1 + (2 * 3));
        return;
    }
}
```

### Expected AST Structure
The reference creates a nested AST where:
- Expression: `1 + (2 * 3)`
  - term: `1` (numericLiteral)
  - rest[0]:
    - op: "+"
    - term: `(2 * 3)` (groupedExpression containing:
      - Expression:
        - term: `2` (numericLiteral)
        - rest[0]:
          - op: "*"
          - term: `3` (numericLiteral)

### Expected VM Output
```
function Main.main 0
    push constant 1
    push constant 2
    push constant 3
    call Math.multiply 2
    add
    call Output.printInt 1
    pop temp 0
    push constant 0
    return
```

## Differences Between Our Implementation and Reference

### Grammar
- **Our**: ANTLR4
- **Reference**: OHM
- **Impact**: Functional equivalence, different parsing mechanism

### AST Structure
- **Our**: Currently uses visitor pattern to generate direct code
- **Reference**: Generates explicit AST nodes with full structure
- **Impact**: NEEDS ADJUSTMENT - Must generate proper AST

### VM Generation
- **Our**: Direct code emission during visit
- **Reference**: Two-phase: Parse to AST, then generate code from AST
- **Impact**: NEEDS ADJUSTMENT - Must implement proper two-phase compilation

### Span Information
- **Our**: Not currently tracked
- **Reference**: All nodes include span (start, end, line)
- **Impact**: NEEDS ADJUSTMENT - Add span tracking

## Implementation Priorities

### High Priority (AST Compatibility)
1. Update visitor to generate proper AST structure
2. Add span information tracking
3. Use correct termType/nodeType names
4. Match expression structure exactly

### Medium Priority (VM Output)
1. Format indentation (4 spaces)
2. Verify instruction order
3. Test with reference samples

### Low Priority (Enhancements)
1. Performance optimizations
2. Error message improvements
3. Additional diagnostics

## Testing Strategy

1. Parse Seven.jack example
2. Compare generated AST with reference
3. Compare generated VM with reference
4. Test with more complex examples
5. Run full project_11 test suite

## Files to Update

```
jack-compiler/src/
├── compiler_visitor.py      ← Major rewrite needed
├── codegen.py              ← VM formatting updates
└── symbols.py              ← Already compatible
```

## References

- Reference Grammar: `/Users/kpillai/WorkData/Dev/web-ide/simulator/src/languages/grammars/jack.ohm`
- Reference Implementation: `/Users/kpillai/WorkData/Dev/web-ide/simulator/src/languages/jack.ts`
- Test Samples: `/Users/kpillai/WorkData/Dev/web-ide/projects/build/samples/project_11/`

## Next Steps

1. ✅ Add char type to grammar
2. → Update visitor for AST generation
3. → Update code generator for VM formatting
4. → Test with reference samples
5. → Verify full compatibility

---

**Last Updated**: During compatibility analysis
**Status**: Grammar updated, AST/VM updates in progress
