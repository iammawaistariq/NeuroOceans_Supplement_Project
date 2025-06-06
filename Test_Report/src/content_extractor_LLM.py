from openai import OpenAI
from Test_Report.utils.config import OPENAI_API_KEY
from Test_Report.utils.config import Test_Report_system_prompt


def process_test_report(extracted_text):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": Test_Report_system_prompt},
            {"role": "user", "content": f"Here is the pdf extracted lab test report content {extracted_text}"},
        ],
        temperature = 0.2,
    )

    return response.choices[0].message.content