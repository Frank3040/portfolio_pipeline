
# Database Performance Benchmark: RDBMS vs NoSQL

A comprehensive benchmark suite comparing PostgreSQL (RDBMS) and MongoDB (NoSQL) performance across different data formats (CSV and JSON). This project provides empirical data to inform database technology decisions based on workload characteristics.

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Benchmark Methodology](#benchmark-methodology)
- [Interpreting Results](#interpreting-results)
- [Performance Considerations](#performance-considerations)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

This benchmark suite evaluates the performance characteristics of relational (PostgreSQL) versus document-oriented (MongoDB) databases when handling structured (CSV) and semi-structured (JSON) data formats. The project measures six critical operations: data insertion, index creation, simple queries, nested queries, complex aggregations, and bulk updates.

## Motivation

Selecting the appropriate database technology is a critical architectural decision. This benchmark addresses common questions:

- When should you use a relational database versus a NoSQL solution?
- How does data format (CSV vs JSON) impact performance?
- What are the trade-offs between schema flexibility and query performance?
- How do different databases handle nested data structures?

By providing quantitative measurements across multiple dimensions, this tool enables data-driven technology selection.

## Architecture

### Technology Stack

- **Python 3.8+**: Core runtime environment
- **PostgreSQL 15**: Relational database management system
- **MongoDB 7**: Document-oriented NoSQL database
- **Streamlit**: Interactive web interface
- **Plotly**: Data visualization
- **Docker**: Database containerization

### Key Libraries

- `psycopg2`: PostgreSQL adapter with COPY support
- `pymongo`: MongoDB Python driver
- `pandas`: Data manipulation and analysis
- `python-dotenv`: Environment configuration management

## Features

### Benchmark Operations

1. **Insert Performance**: Measures bulk data insertion using native optimization techniques
   - PostgreSQL: COPY command for CSV, batch inserts for JSON
   - MongoDB: Bulk insert with unordered execution

2. **Index Creation**: Evaluates index building time and strategy effectiveness
   - PostgreSQL: B-tree indexes for scalar fields, GIN indexes for JSONB
   - MongoDB: Single and compound indexes, including array indexing

3. **Flat Queries**: Tests simple predicates on scalar fields
   - Filter by age threshold
   - Retrieve full result sets

4. **Nested Queries**: Evaluates performance on nested/array data structures
   - PostgreSQL: LIKE operations on text, JSONB containment operators
   - MongoDB: Regex matching on strings, native array membership

5. **Complex Aggregations**: Measures multi-stage analytical queries
   - Filtering, grouping, aggregation functions
   - Result ordering

6. **Bulk Updates**: Tests mass update operations
   - Conditional updates based on field values
   - Transaction management

### Visualization Capabilities

- Interactive grouped bar charts comparing all configurations
- Detailed result tables with percentage differences
- Winner identification per operation
- CSV export for further analysis
- Comparative analysis across database types and formats

## Prerequisites

### Software Requirements

- Python 3.8 or higher
- Docker and Docker Compose (recommended) OR
- PostgreSQL 15+ and MongoDB 7+ installed locally
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

### Python Dependencies

```
streamlit>=1.28.0
psycopg2-binary>=2.9.0
pymongo>=4.5.0
python-dotenv>=1.0.0
plotly>=5.17.0
pandas>=2.0.0
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/db-benchmark.git
cd db-benchmark
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Database Services

#### Using Docker (Recommended)

```bash
# Start PostgreSQL
docker run -d \
  --name postgres-benchmark \
  -e POSTGRES_PASSWORD=postgres123 \
  -e POSTGRES_DB=benchmark_db \
  -p 5432:5432 \
  postgres:15

# Start MongoDB
docker run -d \
  --name mongo-benchmark \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=mongo123 \
  -p 27017:27017 \
  mongo:7
```

#### Using Docker Compose

```bash
docker-compose up -d
```

### 5. Configure Environment

Create a `.env` file in the project root:

```env
POSTGRES_DB=benchmark_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123

MONGO_DB=benchmark_db
MONGO_USER=admin
MONGO_PASSWORD=mongo123
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | PostgreSQL database name | benchmark_db |
| `POSTGRES_USER` | PostgreSQL username | postgres |
| `POSTGRES_PASSWORD` | PostgreSQL password | Required |
| `MONGO_DB` | MongoDB database name | benchmark_db |
| `MONGO_USER` | MongoDB username | admin |
| `MONGO_PASSWORD` | MongoDB password | Required |

### Benchmark Parameters

Adjust dataset size using the Streamlit interface slider (1,000 to 50,000 records). Larger datasets provide more pronounced performance differences but require more time to complete.

## Usage

### Running the Streamlit Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Running Standalone Benchmark

```bash
python benchmark.py
```

This executes the benchmark with default parameters (5,000 records) and displays results using Plotly.

### Workflow

1. Access the Streamlit interface
2. Select dataset size using the slider
3. Click "Run Benchmark"
4. Wait for completion (time varies by dataset size)
5. Review results in three tabs:
   - **Graficas**: Visual comparison charts
   - **Tablas**: Detailed numeric results
   - **Analisis**: Performance analysis and winner identification

## Benchmark Methodology

### Data Generation

The benchmark generates synthetic data with realistic characteristics:

- **Personal Information**: Random first and last names
- **Demographics**: Age distributed with higher frequency in 25-45 range
- **Location**: 15 major U.S. cities
- **Interests**: 15 hobby categories with variable quantities per record

### CSV Format

Flat structure with comma-separated hobby lists:
```
id,name,age,city,hobbies
1,John Smith,32,New York,reading,sports,music
```

### JSON Format

Structured documents with nested arrays:
```json
{
  "id": 1,
  "name": "John Smith",
  "age": 32,
  "city": "New York",
  "hobbies": ["reading", "sports", "music"],
  "metadata": {
    "created_year": 2023,
    "active": true,
    "score": 7.85
  }
}
```

### Optimization Strategies

#### PostgreSQL

- **CSV**: COPY command for bulk inserts, B-tree indexes on age and city
- **JSON**: Row-by-row inserts to demonstrate overhead, GIN indexes on JSONB fields
- **Query Optimization**: Full result set retrieval to measure actual data transfer overhead

#### MongoDB

- **Both Formats**: Bulk unordered inserts for maximum throughput
- **CSV**: Text search capabilities limited to regex
- **JSON**: Native array indexing for efficient membership queries

### Measurement Approach

- High-precision timing using `time.perf_counter()`
- Full result set retrieval (not just counts) to measure actual overhead
- Transaction boundaries clearly defined
- Separate measurement of index creation to isolate impact

## Interpreting Results

### Expected Performance Characteristics

#### Insert Operations

- **PostgreSQL CSV**: Fastest due to COPY command optimization
- **PostgreSQL JSON**: Slower due to row-by-row processing and JSONB parsing
- **MongoDB**: Fast bulk inserts with minimal schema validation

#### Index Creation

- **PostgreSQL**: Slower for GIN indexes due to inverted index structure
- **MongoDB**: Generally faster index creation

#### Flat Queries

- **PostgreSQL CSV**: Fastest due to native column access
- **PostgreSQL JSON**: Overhead from JSONB extraction and casting
- **MongoDB**: Competitive performance with proper indexing

#### Nested Queries

- **PostgreSQL CSV**: LIKE operations without specialized indexes are slower
- **PostgreSQL JSON**: GIN indexes provide efficient containment checks
- **MongoDB JSON**: Optimal performance with native array operations

#### Complex Aggregations

- **PostgreSQL**: Powerful query optimizer handles multi-stage operations efficiently
- **MongoDB**: Aggregation pipeline provides flexible data processing

#### Updates

- **PostgreSQL CSV**: Direct column updates are efficient
- **PostgreSQL JSON**: JSONB modification has overhead
- **MongoDB**: Atomic update operators are highly efficient

### Decision Matrix

**Choose PostgreSQL when:**
- Data is highly relational with many foreign key relationships
- ACID compliance is critical
- Complex joins and analytical queries are common
- Schema is stable and well-defined

**Choose MongoDB when:**
- Documents are self-contained with few relationships
- Schema flexibility is important
- Horizontal scaling is anticipated
- Working primarily with JSON documents

**Use CSV format when:**
- Data is truly tabular without nesting
- Interoperability with legacy systems is required
- Simple import/export workflows are needed

**Use JSON format when:**
- Data has natural hierarchical structure
- Schema varies across documents
- Application works natively with JSON
- Array operations are common

## Performance Considerations

### Hardware Impact

- SSD vs HDD significantly affects insert and index creation times
- Available RAM impacts query cache effectiveness
- CPU cores influence parallel query execution

### Dataset Size Effects

- Small datasets may not show clear differences due to caching
- Recommended minimum: 5,000 records
- Optimal demonstration: 20,000+ records

### Concurrent Load

This benchmark measures single-threaded performance. Production systems under concurrent load will show different characteristics, particularly:
- MongoDB may show better scaling under concurrent writes
- PostgreSQL connection pooling becomes more critical
- Lock contention affects both systems differently

## Project Structure

```
db-benchmark/
├── app.py                  # Streamlit web interface
├── benchmark.py            # Core benchmark logic
├── data_generator.py       # Synthetic data generation
├── .env                    # Environment configuration (not in repo)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Database orchestration
├── data/                   # Generated data files (gitignored)
├── logs/                   # Application logs (gitignored)
└── README.md              # This file
```

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes with clear messages
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request with detailed description

### Areas for Contribution

- Additional database systems (MySQL, CouchDB, etc.)
- More complex query patterns
- Concurrent workload simulation
- Memory usage profiling
- Network latency simulation
- Additional data formats (XML, Parquet)

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- PostgreSQL Global Development Group
- MongoDB Inc.
- Streamlit development team
- Open source community

## Citation

If you use this benchmark in academic work, please cite:

```
@software{db_benchmark,
  title={Database Performance Benchmark: RDBMS vs NoSQL},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/db-benchmark}
}
```

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review existing issues before creating duplicates
- Provide minimal reproducible examples
- Include system information and logs

## Roadmap

- [ ] Add MySQL support
- [ ] Implement concurrent workload testing
- [ ] Add memory profiling
- [ ] Create automated CI/CD pipeline
- [ ] Publish performance baseline results
- [ ] Add query plan visualization
- [ ] Implement cost-based recommendations

---

**Note**: Benchmark results are system-dependent. Your results may vary based on hardware, configuration, and system load. Always validate findings in environments similar to your production systems.

# AI Assistance Disclosure

## Project Information
- **Project Name:** Database Performance Benchmark: RDBMS vs NoSQL
- **Date:** October 2, 2025
- **Course:** Visual Modeling Information
- **Program:** Data Engineering
- **Institution:** Universidad Politécnica de Yucatán

## AI Tool Information
- **AI Tool Used:** Claude (Anthropic) - Sonnet 4.5
- **Usage Period:** October 2, 2025
- **Interaction Method:** Conversational prompts with iterative refinement

## Overall Assistance Assessment

### Summary Statistics
- **Overall AI Assistance Level:** 78%
- **Total Project Time:** ~3 hours
- **Time Using AI:** ~2.5 hours
- **AI-Generated Code Lines:** ~850 lines
- **Total Code Lines:** ~950 lines
- **Human-Modified Lines:** ~100 lines

## Detailed Breakdown by Component

### Component-Level Analysis

| Component | Weight | AI Assistance | Contribution | Details |
|-----------|--------|---------------|--------------|---------|
| Core Benchmark Logic (`benchmark.py`) | 40% | 85% | 34% | Complete implementation with iterative corrections |
| Streamlit Interface (`app.py`) | 25% | 90% | 22.5% | Full UI generation with visualization components |
| Data Generator (`data_generator.py`) | 15% | 80% | 12% | Synthetic data generation logic |
| Documentation (`README.md`) | 15% | 95% | 14.25% | Professional technical documentation |
| Configuration (`.env`, setup) | 5% | 60% | 3% | Environment setup guidance |
| **TOTAL** | **100%** | - | **85.75%** | Combined assistance level |

### Assistance Level by Activity Type

#### Level 4: Extensive Assistance (81-100%)

**Code Generation:**
- Initial implementation of all Python modules
- Database connection logic for PostgreSQL and MongoDB
- Query optimization strategies
- Streamlit UI components with tabs and visualizations
- Plotly chart generation
- Complete README.md documentation

**Specific AI-Generated Content:**
- PostgreSQL COPY command implementation
- MongoDB bulk insert operations
- JSONB GIN index creation
- Complex aggregation queries
- Error handling and logging
- Professional markdown documentation structure

#### Level 2: Moderate Assistance (21-50%)

**Problem Solving:**
- Debugging weight distribution error in data generation (AI: 60%)
- Correcting query execution to fetch actual results (AI: 70%)
- Adjusting insert methods to show realistic performance differences (AI: 75%)

**Configuration:**
- Docker setup instructions (AI: 60%)
- Environment variable structure (AI: 50%)

#### Level 1: Minimal Assistance (0-20%)

**Human-Only Contributions:**
- Project concept and objectives (Human: 100%)
- Identification of incorrect benchmark results (Human: 100%)
- Recognition of query execution issues (Human: 100%)
- Decision to use specific database versions (Human: 100%)
- Testing and validation requirements (Human: 100%)

## Primary Use Cases

### 1. Code Generation: 85%
- Complete implementation of benchmark suite
- Database connection management
- Query execution and timing logic
- Data visualization components
- Error handling and edge cases

### 2. Documentation: 95%
- Professional README.md with comprehensive sections
- Code comments and docstrings
- Installation instructions
- Usage examples
- Performance interpretation guides

### 3. Debugging: 70%
- Weight distribution error resolution
- Query execution correction
- Performance measurement fixes
- Multiple iterations to achieve realistic results

### 4. Architecture Design: 60%
- Project structure recommendations
- Module organization
- Separation of concerns (benchmark, UI, data generation)

## Human Contributions

### Conceptualization (100% Human)
- Original project idea: comparing RDBMS vs NoSQL with CSV vs JSON
- Requirement to demonstrate realistic performance differences
- Decision to measure six distinct operations
- Choice of PostgreSQL and MongoDB as representative systems

### Quality Control (100% Human)
- Identification of three major issues in generated code:
  1. Weight distribution mismatch in data generation
  2. Query execution not fetching results
  3. JSON queries showing unrealistic performance
- Testing and validation of fixes
- Iterative refinement through specific feedback

### Technical Direction (100% Human)
- Request for professional GitHub documentation
- Requirement for production-ready code structure
- Specification of optimization techniques to include
- Decision on visualization approach

### Modifications to AI Output (15% of Total Code)
- Testing and validation scripts (not shown)
- Environment-specific configuration adjustments
- Personal deployment notes
- Execution and debugging iterations

## Verification Process

### Code Validation
1. **Syntax Review:** Verified all Python code runs without syntax errors
2. **Logic Testing:** Tested benchmark execution with sample datasets
3. **Performance Validation:** Confirmed realistic performance differences between configurations
4. **Database Connectivity:** Verified connections to both PostgreSQL and MongoDB
5. **Error Handling:** Tested exception scenarios and logging

### Understanding Verification
- **PostgreSQL Optimization:** Understand COPY command advantages and GIN index functionality
- **MongoDB Operations:** Comprehend bulk insert mechanics and aggregation pipeline
- **Benchmarking Methodology:** Grasp timing measurement precision and warm-up considerations
- **Data Generation:** Understand weighted random distribution for realistic datasets

### Output Testing
- Executed benchmark with 1,000, 5,000, and 10,000 records
- Verified CSV format correctness
- Validated JSON structure with nested arrays
- Confirmed index creation impact on query performance

## Self-Assessment Framework Results

### 1. Initiative and Conceptualization: 25%
**Who defined WHAT to do?**
- Student completely defined problem scope and objectives
- AI provided implementation details based on requirements

### 2. Implementation: 85%
**Who did the technical work?**
- AI generated majority of code with student specifications
- Student made critical corrections through iterative feedback

### 3. Understanding and Validation: 35%
**Do you understand what you did?**
- Student understands general concepts and architecture
- Can explain benchmark methodology and optimization strategies
- Some implementation details (GIN indexes, JSONB operators) learned through this project

### 4. Problem Solving: 60%
**Who solved the errors?**
- Student identified all problems through testing
- AI provided solutions based on problem descriptions
- Student validated all fixes

**Self-Assessment Score:** (25 + 85 + 35 + 60) / 4 = 51.25%

## Final Calculation

### Combined Formula Application

```
Final AI Assistance % = (0.25 × Time %) + (0.35 × Content %) + (0.25 × Complexity %) + (0.15 × Self-Assessment Score)
```

**Component Calculations:**
- **Time %:** (2.5 / 3) × 100 = 83.33%
  - Time Contribution: 0.25 × 83.33% = 20.83%

- **Content %:** (850 / 950) × 100 = 89.47%
  - Content Contribution: 0.35 × 89.47% = 31.31%

- **Complexity %:** 75% (Significant to Extensive level)
  - Complexity Contribution: 0.25 × 75% = 18.75%

- **Self-Assessment Score:** 51.25%
  - Self-Assessment Contribution: 0.15 × 51.25% = 7.69%

**Final AI Assistance Percentage:** 20.83% + 31.31% + 18.75% + 7.69% = **78.58%**

**Rounded Final Assessment: 78%**

## Interaction Log Summary

### Session 1: Initial Development (1.5 hours)
- **Objectives:** Create complete benchmark suite
- **AI Usage:** 
  - Tool: Claude Sonnet 4.5
  - Prompts: ~15 exchanges
  - Generated: `benchmark.py`, `app.py`, `data_generator.py`, `README.md`

### Session 2: Bug Fixes (1 hour)
- **Objectives:** Correct weight distribution and query execution
- **AI Usage:**
  - Tool: Claude Sonnet 4.5
  - Prompts: ~8 exchanges
  - Fixed: Data generation logic, query fetch operations

### Session 3: Performance Tuning (0.5 hours)
- **Objectives:** Ensure realistic performance differences
- **AI Usage:**
  - Tool: Claude Sonnet 4.5
  - Prompts: ~5 exchanges
  - Modified: Insert methods, query result retrieval

## Learning Outcomes

### Concepts Learned Through AI Assistance
1. PostgreSQL GIN indexes for JSONB data types
2. MongoDB bulk insert optimization with `ordered=False`
3. Proper use of `psycopg2.extras.execute_batch`
4. JSONB operators (`?`, `->`, `->>`) in PostgreSQL
5. Streamlit session state management
6. Professional technical documentation structure

### Skills Demonstrated Independently
1. Database performance analysis methodology
2. Identification of measurement artifacts
3. Requirement specification for realistic benchmarks
4. Critical evaluation of generated code
5. Systematic debugging approach

## Ethical Considerations

### Transparency
- Full disclosure of AI tool usage and extent
- Detailed breakdown of AI vs human contributions
- Honest assessment of understanding level

### Academic Integrity
- Project serves learning objectives: understanding database performance characteristics
- AI used as a development accelerator, not a replacement for learning
- Student can explain and defend all major design decisions
- Student identified and corrected AI-generated errors

### Appropriate Use Justification
- **High AI percentage (78%) is justified because:**
  1. Project focus is on comparative analysis and methodology, not implementation from scratch
  2. Professional-grade code quality requirements exceed typical coursework
  3. Multiple database systems and optimization techniques demonstrate breadth over depth
  4. Student maintained conceptual control and quality validation
  5. Time constraints necessitated efficient development

## Recommendations for Similar Projects

### For Students
1. Start with clear requirements before engaging AI
2. Test all generated code thoroughly
3. Don't accept first solution—iterate for quality
4. Understand the "why" behind implementation choices
5. Keep detailed logs of all AI interactions

### For Educators
- This project demonstrates extensive AI assistance (78%)
- Appropriate for advanced projects with time constraints
- Student showed strong problem identification and validation skills
- Recommend supplementary oral examination to verify understanding
- Consider this acceptable for professional development projects, not fundamental learning

## Declaration

I declare that:
1. This disclosure accurately represents the AI assistance used in this project
2. I have tested and validated all AI-generated code
3. I understand the core concepts and can explain the methodology
4. I identified and corrected errors in AI-generated content
5. The final product meets the project requirements and learning objectives

**Student Acknowledgment:**
I acknowledge that while AI assistance was extensive (78%), I maintained control over project direction, identified implementation issues, and ensured the final product meets quality and correctness standards. I can explain the benchmark methodology, database optimization strategies, and performance interpretation to demonstrate comprehension of core concepts.

---