from Test_Report.src.extract_pdf_content import pdf_content_extracting
from Test_Report.src.extract_csv_file_content import csv_content_extracting
from Test_Report.src.extract_txt_content import txt_content_extracting
from Test_Report.src.content_extractor_LLM import process_test_report

import json

def read_report(file_url):

    if file_url.endswith(".pdf"):
        report_content = pdf_content_extracting(file_url)

    elif file_url.endswith(".csv"):
        report_content = csv_content_extracting(file_url)

    elif file_url.endswith(".txt"):
        report_content = txt_content_extracting(file_url)
            
    else:
        return "unknown file format"
    
    # if "genetic_test" in file_url:
    #     extracted_test_report_data = process_test_report(report_content, genetics=True)
    
    extracted_test_report_data = process_test_report(report_content)


    # process LLM response - Convert the string to a Python dictionary
    return json.loads(extracted_test_report_data)
    # return extracted_test_report_data

