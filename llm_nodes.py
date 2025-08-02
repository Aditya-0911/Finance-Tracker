import re
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from langchain_core.messages import AIMessage
from parser_and_prompt import parser, prompt
from config import model
from csv_utils import save_expenses_to_csv


def model_node(state):
    latest_human_msg = state.messages[-1].content
    formatted_prompt = prompt.format(input=latest_human_msg)
    output = model.invoke(formatted_prompt)
    parsed = parser.parse(output.content)

    friendly_msg = "Got it!"

    return state.model_copy(update={
        "messages": state.messages + [AIMessage(content=friendly_msg)],
        "expenses": parsed.expense,
        "action": parsed.action
    })

def add_expense_node(state):
    if not state.expenses:
        return state.model_copy(update={
            "messages": state.messages + [AIMessage(content="No expenses to add.")],
        })
    updated_df = save_expenses_to_csv({'expense': state.expenses})
    summary = "\n".join([
        f"Added {e.amount} under '{e.category}' on {e.date.strftime('%d/%m/%Y')}"
        for e in state.expenses
    ])
    return state.model_copy(update={
        "messages": state.messages + [AIMessage(content=summary)],
        "df": updated_df
    })

def summarize_node(state):
    try:
        df = pd.read_csv("expenses.csv", parse_dates=["date"])
    except FileNotFoundError:
        return state.model_copy(update={"messages": state.messages + [AIMessage(content="No data found.")]})

    if df.empty:
        return state.model_copy(update={"messages": state.messages + [AIMessage(content="No expenses available to summarize.")]})

    last_user_message = [msg for msg in state.messages if msg.type == "human"][-1].content
    match = re.search(r"last\s+(\d+)\s+transactions", last_user_message, re.IGNORECASE)
    if not match:
        return state.model_copy(update={"messages": state.messages + [AIMessage(content="Please specify like 'last 5 transactions'.")]})

    n = int(match.group(1))
    filtered_df = df.sort_values(by="date", ascending=False).head(n)

    if filtered_df.empty:
        return state.model_copy(update={"messages": state.messages + [AIMessage(content="No matching expenses found.")]})

    prompt = f"Summarize these last {n} transactions:\n\n{filtered_df.to_string(index=False)}. The amount is in INR"
    llm_response = model.invoke(prompt)

    # Plot to buffer
    buf = BytesIO()
    plt.figure(figsize=(6, 6))
    filtered_df.groupby("category")["amount"].sum().plot.pie(autopct='%1.1f%%', startangle=140, shadow=True)
    plt.ylabel("")
    plt.title(f"Category Breakdown of Last {n} Transactions")
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return state.model_copy(update={
        "messages": state.messages + [AIMessage(content=llm_response.content)],
        "plot_bytes": buf.read()
    })