from typing import Optional, Union, List, Literal
import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from langchain_core.messages import HumanMessage, AIMessage
import pandas as pd
import dateparser

class Expense(BaseModel):
    amount: float = Field(..., gt=0)
    category: str = Field(...)
    date: Optional[datetime.date] = Field(None)

    @field_validator("category")
    def clean_category(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("date", mode="before")
    def parse_date(cls, v):
        if v is None:
            return None  # We'll fill this in later with a model_validator

        if isinstance(v, datetime.date):
            return v

        if isinstance(v, str):
            v_clean = v.strip().lower()
            today = datetime.date.today()

            if v_clean == "today":
                return today
            elif v_clean == "yesterday":
                return today - datetime.timedelta(days=1)
            elif v_clean == "tomorrow":
                return today + datetime.timedelta(days=1)

            # Try standard formats
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y"):
                try:
                    return datetime.datetime.strptime(v_clean, fmt).date()
                except ValueError:
                    continue

            # Fallback to dateparser
            parsed = dateparser.parse(v_clean)
            if parsed:
                return parsed.date()

        raise ValueError(f"Invalid date format: {v}. Use 'today', '3 days ago', or 'DD/MM/YYYY'.")

    @model_validator(mode="after")
    def set_default_date(cls, values):
        if values.date is None:
            values.date = datetime.date.today()
        return values

class ExpenseList(BaseModel):
    expense: List[Expense]
    action:str

class AgentState(BaseModel):
    messages: List[Union[HumanMessage, AIMessage]] = []
    action: Optional[Literal["add_expense", "summarize"]] = None
    expenses: Optional[List[Expense]] = None
    df: Optional[pd.DataFrame] = None 
    plot_bytes: Optional[bytes] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)