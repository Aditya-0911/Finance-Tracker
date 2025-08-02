# 💸 LangGraph Expense Tracker

A smart, LLM-powered expense tracking system built with **LangGraph**, **LangChain**, and **Streamlit**. This app allows users to log expenses in natural language and summarize them with visual breakdowns — all in a chat interface.

---

## ✨ Features

- 🧠 **LLM-Powered Parsing**: Extracts amount, category, and date from user input like `"I spent 200 on groceries today"` using LangChain models.
- 📊 **Visual Summaries**: Generates a category-wise pie chart of the last *n* expenses (e.g., "summarize last 5 transactions").
- 💬 **Conversational Interface**: Built with Streamlit’s chat UI for a smooth and interactive experience.
- 🔁 **Graph-based Workflow**: Modular LangGraph handles routing and node execution flow.

---

## ⚙️ Architecture

The system is built using a LangGraph with the following structure:

![LangGraph Flow](graph.png)

### Flow Description

1. `model` node: Parses user input and extracts structured data.
2. `Router` node: Routes the action to either:
   - `add_node`: Adds expense to CSV (or future Google Sheet integration).
   - `summarize_node`: Summarizes last *n* transactions and plots a pie chart.
3. Ends by updating the chat state.
