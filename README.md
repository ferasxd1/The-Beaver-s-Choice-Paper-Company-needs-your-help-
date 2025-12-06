#  Beaver's Choice Paper Company - Multi-Agent System

A comprehensive multi-agent AI system for intelligent inventory management, quote generation, and sales processing.

##  Project Overview

This project implements an intelligent multi-agent system to revolutionize the operations of Beaver's Choice Paper Company. The system handles customer inquiries, manages inventory levels, generates competitive quotes, and processes sales transactions through coordinated AI agents.

##  System Architecture

The system consists of **4 specialized agents**:

1. **Orchestrator Agent** - Central coordinator that routes requests
2. **Inventory Agent** - Manages stock levels and reordering
3. **Quoting Agent** - Generates competitive price quotes
4. **Sales Agent** - Finalizes transactions and order fulfillment

##  Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
pip install smolagents litellm

# Configure environment
cp .env.example .env
# Edit .env and add your UDACITY_OPENAI_API_KEY
```

### Running the System

```bash
# Navigate to src folder
cd src

# Run the system
python main.py
```

##  Project Structure

```
 Beaver's Choice Multi-Agent System

  requirements.txt                # Python dependencies
  .env.example                    # Environment template
  .gitignore                      # Git ignore rules
  README.md                       # Project documentation
  PROJECT_STRUCTURE.md            # Detailed structure guide
  project_starter.py              # Legacy helper functions

  src/                            # Source Code (Organized!)
    __init__.py                    # Package initialization
    main.py                        # Main entry point
    agents.py                      # Agent definitions
    tools.py                       # Agent tools (9 tools)
    utils.py                       # Helper functions

  docs/                           # Documentation & Diagrams
     PROJECT_REPORT.md           # Comprehensive report (19 KB)
     agent_workflow_diagram.png  # Visual workflow (517 KB)
     agent_workflow_diagram.md   # Workflow description

  data/                           # Data Files
     quote_requests.csv          # All customer requests (30 KB)
     quote_requests_sample.csv   # Test dataset (19 requests)
     quotes.csv                  # Historical quotes (57 KB)

  results/                        # Test Results
      test_results.csv            # Evaluation output (16 KB)
```

##  Features

- ** 4 Specialized AI Agents** working in harmony
- ** Intelligent Decision Making** using historical data
- ** Smart Pricing** with automatic bulk discounts (5%, 10%, 15%)
- ** Real-time Financial Tracking** of cash and inventory
- ** Automated Reordering** when stock is low
- ** Professional Communication** with customers

##  Technology Stack

- **Framework**: smolagents v1.23.0
- **LLM Model**: GPT-4o-mini (via Vocareum)
- **Database**: SQLite with SQLAlchemy
- **Language**: Python 3.10+

##  Documentation

- [PROJECT_REPORT.md](docs/PROJECT_REPORT.md) - Complete system documentation
- [agent_workflow_diagram.md](docs/agent_workflow_diagram.md) - Detailed workflow
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Directory structure guide

##  Key Achievements

-  4 specialized agents working in coordination
-  9 tools utilizing all helper functions
-  Intelligent quote generation with discounts
-  Automated inventory management
-  Real-time financial tracking
-  Professional customer communication

##  Author

**Feras Khairallah**
- GitHub: [@ferasxd1](https://github.com/ferasxd1)

---

**Made with  and **
