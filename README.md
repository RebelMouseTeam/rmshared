# RebelMouse Content Taxonomy System

## Introduction

The RebelMouse Content Taxonomy System is a sophisticated, entity-agnostic filtering and classification framework designed to handle complex content queries across diverse data structures. Built on functional programming principles and the visitor pattern, it provides a unified approach to content filtering, variable templating, and tree traversal operations.

The system operates on a fundamental principle: **entity-agnostic design**. Rather than being tied to specific content types (posts, sections, users), it works with abstract entities defined by field-value mappings. This allows the same filtering logic to be applied consistently across different content domains while maintaining type safety and performance.

### System Architecture Overview

The taxonomy system has evolved through multiple chapters of development:

1. **Chapter I**: Core filtering primitives - filters, labels, ranges, fields, and entities
2. **Chapter II**: Template variables system with operators and dynamic filter construction  
3. **Chapter III**: Advanced traversal infrastructure with visitor patterns for tree analysis

Each chapter builds upon the previous, creating a mature platform capable of handling RebelMouse's complex content filtering requirements while maintaining clean architecture and comprehensive functionality.

## Chapter I: Core Filtering Primitives

### Entity-Based Foundation

Every content item in RebelMouse is represented as an `IEntity` - a mapping from field names to sets of values with well-defined cardinality constraints:

- **0..1**: Optional single value fields (e.g., publish date)
- **1..1**: Required single value fields (e.g., content ID)
- **0..M**: Optional multi-value fields (e.g., tags)
- **1..M**: Required multi-value fields (e.g., categories)

### Label-Based Filtering

The system uses three types of labels for precise entity matching:

- **`Value(field, value)`**: Exact field-value pairs for precise matching
- **`Badge(field)`**: Field existence checks regardless of value
- **`Empty(field)`**: Field absence validation for negative conditions

### Filter Logic Composition

Filters combine using mathematical set operations:

- **`AnyLabel(labels)`**: OR operation - entity matches if it satisfies any label
- **`NoLabels(labels)`**: NOT operation - entity matches if it satisfies no labels
- **`AnyRange(ranges)`**: OR operation for range-based queries
- **`NoRanges(ranges)`**: NOT operation for range-based queries

### Range-Based Queries

Monotonic fields support temporal and numerical filtering:

- **`Between(field, min_value, max_value)`**: Inclusive range queries
- **`LessThan(field, value)`**: Upper bound filtering
- **`MoreThan(field, value)`**: Lower bound filtering

### Real Example: Content Filtering

Here's a comprehensive filtering example showing a complete filter tree structure:

```
Root Filter (AND logic - all must match)
├── AnyLabel: published OR featured content
│   ├── Value(System("status"), "published")
│   └── Badge(System("is_featured"))
├── NoLabels: exclude videos AND must have sections
│   ├── Value(System("content_type"), "video")
│   └── Empty(System("sections"))
├── AnyRange: recent OR high-engagement content
│   ├── MoreThan(System("modified_at"), "2024-01-01")
│   └── Between(System("view_count"), 1000, 50000)
├── NoRanges: exclude old low-engagement content
│   ├── LessThan(System("created_at"), "2023-01-01")
│   └── LessThan(System("engagement_score"), 100)
└── AnyLabel: custom client filtering
    ├── Value(Custom("extras", "category.priority"), "high")
    ├── Badge(Custom("roar_specific_data", "marketing.promoted"))
    └── Empty(Custom("site_specific_data", "restrictions.geo"))
```

This filter tree demonstrates:
- **Entity-agnostic filtering** across system and custom fields
- **All label types**: Value (exact matching), Badge (presence), Empty (absence)
- **All filter types**: AnyLabel (OR), NoLabels (NOT), AnyRange (OR), NoRanges (NOT)
- **Range operations** with inclusive boundaries for temporal and numerical data
- **System vs custom fields** with unified processing
- **Complex tree structure** with set operations and monotonic value filtering

## Chapter II: Template Variables System

### Dynamic Filter Construction

Chapter II introduces a powerful templating system that allows dynamic filter construction using `Switch`/`Return` operators with variable substitution, enabling reusable filter patterns across different contexts.

### Operators and Variables

**Core Template Operators**:
- **`Switch(ref, cases)`**: Conditional branching based on variable values
- **`Return(cases)`**: Terminal operator that returns concrete filter cases

**Variable References**:
- **`Reference(alias)`**: Named variable placeholders for runtime substitution
- **Variable resolution**: Templates resolve to concrete filters based on context

### Arguments and Type Matching

Template operators use argument types for pattern matching:
- **`arguments.Any`**: Matches any variable value (default case)
- **`arguments.Value`**: Matches specific values in switch statements
- **`arguments.Type`**: Matches by variable type for complex routing

### Real Example: Dynamic Content Templates

Here's a comprehensive blog post filtering template based on real-world patterns:

```
Blog Post Filtering Template (Real-world patterns from tests)
├── Return: Static post identification
│   └── AnyLabel
│       └── Return
│           └── Value(System("post-id"), Constant(123))
├── Switch(ref="some_section_id")
│   ├── Any: No section filtering (show all)
│   │   └── Return
│   │       └── [] (empty cases)
│   ├── Empty: Posts with no regular section  
│   │   └── Return
│   │       └── AnyLabel
│   │           └── Return
│   │               └── Empty(System("post-regular-section"))
│   └── Value: Posts in specific section
│       └── Return
│           └── AnyLabel
│               └── Return
│                   └── Value(System("post-regular-section"), Variable("some_section_id", index=1))
├── Return: Privacy filtering
│   └── AnyLabel
│       └── Return
│           └── Badge(System("private-post"))
├── Switch(ref="some_tag_slug")
│   ├── Any: Fallback to post-id matching
│   │   └── Return
│   │       └── AnyLabel
│   │           └── Return
│   │               └── Value(System("post-id"), Constant(123))
│   ├── Empty: Posts with no primary tag
│   │   └── Return
│   │       └── AnyLabel
│   │           ├── Return
│   │           │   └── Value(System("post-id"), Constant(123))
│   │           └── Return
│   │               └── Empty(System("post-primary-tag"))
│   └── Value: Posts with specific tag
│       └── Return
│           └── AnyLabel
│               ├── Return
│               │   └── Value(System("post-id"), Constant(123))
│               └── Return
│                   └── Value(System("post-primary-tag"), Variable("some_tag_slug"))
└── Switch(ref="published_at_range"): Cross-variable references
    └── Value: Complex temporal filtering
        └── Return
            ├── AnyRange: Modified time window
            │   └── Return
            │       └── Between(System("post-modified-at"), 
            │                   min_value=Variable("published_at_range", index=1), 
            │                   max_value=Variable("published_at_range", index=2))
            └── NoRanges: Exclude recent modifications + old publications
                ├── Return
                │   └── MoreThan(System("post-modified-at"), 
                │               value=Variable("published_at_range", index=1))
                └── Return
                    └── Between(System("post-published-at"), 
                                min_value=Constant(100), 
                                max_value=Variable("published_at_range", index=2))
```

This template demonstrates:
- **Cross-variable references** with tuple destructuring using 1-based indexing
- **Meaningful fallback logic** where `Any` cases provide sensible defaults vs empty cases
- **Mixed static/dynamic filtering** combining constants with variable substitution
- **Universal Return wrapping** for future extensibility at every level
- **Complex conditional logic** with Switch operators enabling type-based branching
- **Real-world patterns** from actual test fixtures showing practical usage

### Variables → Core Integration

Variables traverse through operator logic and ultimately delegate to core filtering. The operator traversal system processes `Switch`/`Return` logic and delegates resolved cases to core traversal components, enabling template variable resolution with full core filtering capabilities.

The integration pattern ensures that template variables can leverage the complete power of the core filtering system while adding dynamic behavior through conditional operators.

## Chapter III: Tree Traversal Infrastructure

### Advanced Visitor Pattern Architecture

Chapter III introduces sophisticated traversal and visitor pattern infrastructure that provides powerful tree analysis, validation, and processing capabilities across both core and variables layers.

### Traversal Engine Components

**Core Traversal Components**:
- `core.traversal.filters.Filters` - Orchestrates complex filter tree traversal with nested label and range processing
- `core.traversal.labels.Labels` - Handles label tree traversal with field and value delegation
- `core.traversal.ranges.Ranges` - Manages range tree traversal with field and value delegation
- `core.traversal.events.Events` - Provides simple event enter/leave processing

**Variables Traversal Components**:
- `variables.traversal.operators.Operators` - Central operator processing with recursive switch/return logic
- `variables.traversal.filters.Filters` - Delegates filter traversal to core through operator pattern
- `variables.traversal.labels.Labels` - Delegates label traversal to core through operator pattern
- `variables.traversal.ranges.Ranges` - Delegates range traversal to core through operator pattern

### Visitor Pattern Implementation

**Visitor Interface Hierarchy**:

**Core Interfaces**:
- `IFilters`, `ILabels`, `IRanges`, `IEvents` - Enter/leave patterns for tree node processing
- `IFields`, `IValues` - Visit patterns for leaf node processing

**Variables Interfaces**:
- `IOperators` - Enter/leave patterns for Switch/Return operator processing
- `IArguments` - Visit patterns for argument type processing
- `IValues` - Visit patterns for constants and variable processing

### Visitor Delegation Architecture

Each visitor class implements clean delegation with runtime type checking:

```python
class Filters(IFilters):
    def __init__(self, delegate: Any):
        self.delegate = delegate
    
    def enter_filter(self, filter_):
        isinstance(self.delegate, IFilters) and self.delegate.enter_filter(filter_)
    
    def leave_filter(self, filter_):
        isinstance(self.delegate, IFilters) and self.delegate.leave_filter(filter_)
```

### Real Example: Complete Tree Traversal

Here's a comprehensive traversal example demonstrating visitor pattern capabilities:

```python
class AnalysisVisitor:
    """Multi-interface visitor for comprehensive filter tree analysis"""
    
    def __init__(self):
        self.visits = []
        self.filter_count = 0
        self.field_usage = {}
        self.depth = 0
    
    def enter_filter(self, filter_):
        self.visits.append(('enter_filter', type(filter_).__name__, self.depth))
        self.filter_count += 1
        self.depth += 1
    
    def leave_filter(self, filter_):
        self.depth -= 1
        self.visits.append(('leave_filter', type(filter_).__name__, self.depth))
    
    def enter_label(self, label):
        self.visits.append(('enter_label', type(label).__name__, self.depth))
        self.depth += 1
    
    def leave_label(self, label):
        self.depth -= 1
        self.visits.append(('leave_label', type(label).__name__, self.depth))
    
    def visit_field(self, field):
        self.visits.append(('visit_field', field.name, self.depth))
        self.field_usage[field.name] = self.field_usage.get(field.name, 0) + 1
    
    def visit_value(self, value):
        self.visits.append(('visit_value', str(value), self.depth))
    
    def enter_operator(self, operator):
        self.visits.append(('enter_operator', type(operator).__name__, self.depth))
        self.depth += 1

# Example traversal output for complex filter tree:
# [
#   ('enter_filter', 'AnyLabel', 0),
#   ('enter_label', 'Value', 1), 
#   ('visit_field', 'author', 2),
#   ('visit_value', 'john', 2),
#   ('leave_label', 'Value', 1),
#   ('enter_label', 'Badge', 1),
#   ('visit_field', 'featured', 2), 
#   ('leave_label', 'Badge', 1),
#   ('leave_filter', 'AnyLabel', 0)
# ]
#
# Analysis results:
# - filter_count: 4 (complexity metric)
# - field_usage: {'author': 2, 'featured': 1, 'date': 1, 'views': 1}
# - visits: Complete traversal sequence with depth tracking
```

### Factory and Assembly Patterns

**Traversal Factory System**:
- `core.traversal.factory.Factory` - Creates configured traversal components
- `variables.traversal.factory.Factory` - Creates variable traversal components  
- `core.traversal.assembler.Assembler` - Assembles complete systems with dependencies
- `variables.traversal.assembler.Assembler` - Assembles variable systems with core delegation

**Composite Traversal Pattern**:
- `core.traversal.composite.Composite` - Unified interface for all traversal operations
- Provides single entry point for complex multi-type traversal scenarios
- Handles automatic visitor routing based on content type

### Key Technical Achievements

#### 1. **Unified Traversal Interface**
- Single traversal API works across all filter types, operators, and variable constructs
- Consistent visitor pattern implementation across all components
- Type-safe delegation with runtime interface checking

#### 2. **Flexible Visitor Composition**
- Visitors can implement any combination of interfaces based on processing needs
- Clean separation between tree node processing (enter/leave) and leaf processing (visit)
- Runtime safety through `isinstance()` checks without complex inheritance

#### 3. **Seamless Variables Integration**
- Template variables (`Switch`/`Return`) transparently resolve to core filter operations
- Variable traversal maintains full core traversal capabilities
- Operator processing delegates resolved cases to appropriate core traversers

#### 4. **Production-Ready Architecture**
- Factory patterns enable easy configuration and dependency injection
- Composite patterns provide unified interfaces for complex scenarios
- Individual visitor classes eliminate complex interface dependencies
- Enhanced flexibility through selective interface implementation

### Foundation for Advanced Operations

The Chapter III traversal infrastructure provides a solid foundation for sophisticated taxonomy operations:

- **Tree Analysis**: Visitor patterns enable filter tree complexity analysis and optimization
- **Validation Systems**: Easy to add constraint validation visitors across complete filter trees
- **Code Generation**: Traversal patterns support generating optimized database query code
- **Debugging Tools**: Comprehensive visitor logging enables detailed traversal debugging and profiling
- **Performance Optimization**: Factory patterns allow for cached or memoized traverser instances
- **Advanced Analytics**: Tree analysis capabilities for usage pattern detection and performance profiling

This mature traversal system balances flexibility, performance, and maintainability while providing comprehensive coverage of RebelMouse's complex content taxonomy requirements.

## Chapter IV: SQL Parsing & Compiling

### SQL Query Generation Architecture

Chapter IV introduces a comprehensive SQL compilation system that transforms the taxonomy filter trees into executable SQL queries. This system provides a bridge between the abstract filter operations and concrete database operations, enabling high-performance content queries at scale.

### Core SQL Components

**Foundation Layer (`rmshared.sql`)**:
- `parsing` - Converts SQL variations into taxonomy filters using Lark grammar-based parsing with support for numbers, strings, and complex expressions  
- `compiling` - Generates SQL from taxonomy filters, labels, ranges, and other constructs using abstract syntax tree compilation with terminal nodes, operations, logical operators, and conditional structures
- Advanced compaction system with customizable connectors and break handling for optimized SQL generation

**Taxonomy Integration (`rmshared.content.taxonomy.sql`)**:
- `descriptors` - Entity field definitions, scope management, and registry pattern for taxonomy-aware SQL generation
- `parsing` - Converts taxonomy-specific SQL syntax to filters using Lark grammar supporting variable references, field expressions, and filter operations
- `compiling` - Generates SQL from taxonomy structures using high-level `Compiler` class that orchestrates the transformation

**Core SQL Compilation (`rmshared.content.taxonomy.core.sql.compiling`)**:
- `assembler` - Factory pattern for assembling complete SQL compilation systems
- `factory` - Dependency injection for configurable compilation components
- `composite` - Unified interface combining all compilation capabilities
- `filters`, `labels`, `ranges` - Specialized compilers for different taxonomy concepts
- `fields`, `values`, `events` - SQL generation for taxonomy primitives

**Variables SQL Compilation (`rmshared.content.taxonomy.variables.sql.compiling`)**:
- `operators` - Switch/Return operator compilation to conditional SQL structures
- `variables` - Variable reference resolution and SQL parameter binding
- Template-based SQL generation with dynamic parameter substitution

### SQL Grammar Support

The system supports comprehensive SQL-like syntax through Lark grammars:

**Basic Types and Expressions**:
```sql
-- Taxonomy scope references
posts.title, users.email, sections.name

-- Field operations with variables
posts.status IS @status_variable
posts.created_at BETWEEN @start_date AND @end_date
posts.tags CONTAIN ANY ('tech', 'news', @dynamic_tag)

-- Custom field access
CUSTOM_FIELD('extras.priority') IS 'high'
CUSTOM_FIELD("site_specific_data.category") NOT IN (@excluded_categories)

-- Complex conditional filters
posts.featured IS TRUE IF @show_featured IS NOT NULL
posts.section IS @section_id IF @section_id IS NOT NULL OTHERWISE posts.featured IS TRUE
```

### Advanced SQL Features

**Variable Reference System**:
- `@@1`, `@@2` - Positional variable references by index
- `@variable_name` - Named variable references with optional array indexing
- `@variable_name[1]` - Array element access with 1-based indexing for tuple variables
- Dynamic SQL parameter binding with type-safe variable resolution

**Filter Compilation Patterns**:
- Label filters → SQL WHERE conditions with field existence checks
- Range filters → SQL comparison operators with inclusive/exclusive boundary handling
- Badge filters → Boolean field presence checks with NULL handling
- Empty filters → Explicit NULL or empty collection checks

**Entity Relationship Management**:
- Scope-based table aliasing (`posts`, `users`, `sections`, `communities`, `tags`)
- Cross-entity relationship queries with proper JOIN generation
- ID field resolution with entity-specific primary key mapping
- Custom field path resolution for nested JSON/document structures

### Real Example: Complete SQL Compilation

Here's how a complex taxonomy filter compiles to SQL:

**Input Taxonomy Filter**:
```python
AnyLabel([
    Value(System("status"), Variable("post_status")),
    Badge(System("featured"))
])
```

**Generated SQL Output**:
```sql
(posts.status = @post_status OR posts.featured IS NOT NULL)
```


### Integration Architecture

**Unified Compiler Interface**:
```python
from rmshared.content.taxonomy.sql import Compiler

compiler = Compiler()

# Entity scope resolution
scope_tree = compiler.make_tree_from_scope(posts.guids.Post)  # → "posts"

# Field compilation  
field_tree = compiler.make_tree_from_field(System("title"))   # → "posts.title"

# Filter compilation
filter_tree = compiler.make_tree_from_constant_filter(filter_) # → SQL WHERE clause

# Variable template compilation
variable_tree = compiler.make_tree_from_variable_filter(template) # → Conditional SQL
```

**Factory Pattern Integration**:
- Descriptor registry provides field metadata and validation rules
- Factory classes enable dependency injection and system configuration
- Assembler pattern combines core and variables compilation capabilities
- Composite pattern provides unified interface for all SQL generation operations

### Performance and Optimization

**SQL Optimization Features**:
- Tree compaction eliminates redundant parentheses and whitespace
- Parameterized query generation prevents SQL injection while enabling prepared statements
- Entity relationship optimization with minimal JOIN operations
- Custom field path optimization for document database queries

**Scalability Considerations**:
- Lazy compilation with cached SQL tree generation
- Memory-efficient tree structures with minimal object overhead  
- Type-safe variable binding with compile-time validation
- Modular architecture enables horizontal scaling of SQL generation

The SQL compilation system represents a mature bridge between RebelMouse's abstract taxonomy operations and concrete database performance, enabling sophisticated content queries while maintaining the flexibility and safety of the taxonomy architecture.
