

# **Product Requirements Document (PRD)**

---

### **1\. Introduction**

#### **1.1 Project Goal**

Develop an open-source service of autonomous AI agents that automates in-depth research and complex task execution based on a user-selected topic. The service will be entirely free to use, support local LLMs running within a Docker-based Ollama container, and use the Tavily Search API for data collection.

#### **1.2 Objectives**

* Design a flexible architecture that allows agents to operate autonomously, collaborate with one another, and execute multi-step tasks.  
* Implement key agent modules: **Manager**, **Researcher**, **Writer**, **Critic**, and **Programmer**.  
* Integrate local LLM support via a Docker-based **Ollama** container.  
* Utilize the **Tavily Search API** as the primary tool for internet research.  
* Provide a simple, intuitive user interface for managing the process and viewing results.

---

### **2\. Functional Requirements**

#### **2.1 Core Features**

* **Task Initiation**: The user provides a topic and a goal (e.g., "Research the European solar panel market for 2024 and write a SWOT analysis").  
* **Task Decomposition**: The Manager agent automatically breaks down the user's request into granular subtasks using an LLM.  
* **Task Assignment**: The Manager assigns each subtask to the appropriate agent.  
* **Autonomous Execution**: Agents independently perform their assigned tasks, exchanging data through an internal system.  
* **Report Generation**: The system compiles results from all agents into a final report, which can be refined by the Writer agent and reviewed by the Critic agent.  
* **Interactive Progress View**: The user can track the progress, view intermediate results, and see the final report via a web-based UI.

#### **2.2 Agent Roles**

##### **2.2.1 Manager Agent**

* **Functions**: Receives user requests, decomposes tasks, assigns subtasks, oversees execution, and assembles the final output.  
* **Input**: User's text query.  
* **Output**: A structured list of tasks for other agents.

##### **2.2.2 Researcher Agent**

* **Functions**: Gathers information from the internet.  
* **Tools**: **Tavily Search API**.  
* **Input**: A subtask from the Manager (e.g., "Collect data on solar panel sales in Germany").  
* **Output**: A structured report with raw data, source URLs, and a brief summary.

##### **2.2.3 Writer Agent**

* **Functions**: Creates a cohesive and structured report or article based on data provided by other agents.  
* **Tools**: LLM for text generation.  
* **Input**: Structured data from the Researcher agent and instructions from the Manager.  
* **Output**: The final report text in **Markdown** or plain text format.

##### **2.2.4 Critic Agent**

* **Functions**: Analyzes results (reports, code), identifies weaknesses, and generates new tasks for improvement.  
* **Tools**: LLM for content analysis.  
* **Input**: An intermediate report, code, or other result.  
* **Output**: A list of suggestions and new subtasks for the Manager agent.

##### **2.2.5 Programmer Agent**

* **Functions**: Writes and executes code (scripts) to solve specific tasks (e.g., data analysis).  
* **Tools**: LLM for code generation, a **Python interpreter** for secure code execution.  
* **Input**: A subtask from the Manager (e.g., "Write a Python script to calculate the average sales value").  
* **Output**: The executed code and its result.

---

### **3\. Technical Requirements**

#### **3.1 Technologies**

* **Framework**: **LangChain**.  
* **Programming Language**: **Python**.  
* **Local LLM**: **Ollama** (Docker image).  
* **Search API**: **Tavily Search API**.  
* **Database**: **SQLite**.  
* **UI**: **Streamlit** or **Gradio**.

#### **3.2 System Architecture**

The architecture will be based on microservices, where each agent is a separate module.  
.

1. **User Interface (UI)**: Sends the user's request to the Manager agent.  
2. **Manager Agent**: Receives the request and uses an LLM to create a plan.  
3. **Orchestration**: The Manager assigns tasks to other agents.  
4. **Agent Services**: Agents perform their tasks, interacting with external tools (Tavily, code interpreter) and the LLM.  
5. **Data Storage**: All intermediate results, reports, and history are stored in an SQLite database.

---

### **4\. Decomposed Tasks for Implementation**

Each task is broken down into atomic, self-contained units that can be implemented with the help of an LLM.

#### **4.1 Core Development**

* **Task A: Docker Configuration:** Create a docker-compose.yml to orchestrate app and ollama services.  
* **Task B: Core Initialization:** Write main.py to initialize the LLM, Tavily API, and SQLite database connection, along with the Streamlit UI.

#### **4.2 Manager Agent**

* **Task A: Task Decomposition Logic:** Create a module with a function decompose\_task(user\_query) that uses a LangChain prompt to break down the request into a structured JSON list of tasks.  
* **Task B: Orchestration Logic:** Implement a function orchestrate\_agents(tasks) to manage the workflow, calling the appropriate agent for each task and updating the database.

#### **4.3 Researcher Agent**

* **Task A: Tavily Tool Creation:** Create a LangChain tool TavilySearchTool to wrap the Tavily API.  
* **Task B: Agent Logic:** Define a prompt for the agent to use the TavilySearchTool to find and synthesize information into a structured report.

#### **4.4 Writer Agent**

* **Task A: Agent Logic:** Create a module with a prompt for the agent to transform raw data into a cohesive and well-structured Markdown report.

#### **4.5 Critic Agent**

* **Task A: Agent Logic:** Create a module with a prompt for the agent to evaluate reports or code, identify weaknesses, and propose new tasks in a JSON format.

#### **4.6 Programmer Agent**

* **Task A: Secure Code Execution:** Implement a SandboxExecutor class to run Python code safely.  
* **Task B: Agent Logic:** Define a prompt for the agent to generate Python code and use the SandboxExecutor to run it, returning the result.

---

### **5\. Roadmap**

* **Phase 1 (MVP)**: Implement the Manager and Researcher agents to provide a basic, functional prototype.  
* **Phase 2 (Expansion)**: Add the Writer, Critic, and Programmer agents and establish the feedback loop.  
* **Phase 3 (Optimization)**: Improve agent performance and add more advanced use cases.  
* **Phase 4 (Community)**: Publish the project on GitHub with detailed documentation and build a community around it.