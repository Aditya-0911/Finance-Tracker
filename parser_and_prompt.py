from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from models import ExpenseList
from constants import ALLOWED_CATEGORIES, action_list

parser = PydanticOutputParser(pydantic_object=ExpenseList)

prompt = PromptTemplate(
    template="""Extract all expenses from the text below.
Each expense should include:
- amount (float)
- category (must be one of: {category_list})
- date (use natural phrases like "today", "yesterday", or a date like "29/07/2025")

If a date is shared, apply it to all expenses.
Map ambiguous terms to the best-fit category from the list.
You shall also classify the action of the user input from these action categories {actions}

Text:
{input}

{format_instructions}
""",
    input_variables=["input"],
    partial_variables={
        "category_list": ", ".join(ALLOWED_CATEGORIES),
        "actions": ", ".join(action_list),
        "format_instructions": parser.get_format_instructions()
    }
)
