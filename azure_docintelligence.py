import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import  AnalyzeResult
from dotenv import load_dotenv

load_dotenv()

# Fetch endpoint and API key from environment variables
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")
# Initialize the client
client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
print(client)
# URL of the document to analyze
url = ".\\data\\flowchart (26).png"

def get_words(page, line):
    return [word for word in page.words if _in_span(word, line.spans)]

def _in_span(word, spans):
    for span in spans:
        if span.offset <= word.span.offset < span.offset + span.length:
            return True
    return False

try:
    # Start document analysis'

    with open (url,"rb") as content:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=content,
            # AnalyzeDocumentRequest(url_source=url),
            content_type="application/octet-stream",
        )

    result: AnalyzeResult = poller.result()

    if result.styles and any(style.is_handwritten for style in result.styles):
        print("Document contains handwritten content")
    else:
        print("Document does not contain handwritten content")

    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
        print(f"Page dimensions: {page.width} x {page.height} {page.unit}")

        for line_idx, line in enumerate(page.lines):
            words = get_words(page, line)
            print(f"...Line #{line_idx} has {len(words)} words: '{line.content}'")

            for word in words:
                print(f"......Word '{word.content}' has a confidence of {word.confidence}")

        for selection_mark in page.selection_marks:
            print(f"Selection mark: '{selection_mark.state}' at {selection_mark.polygon}")

    for table_idx, table in enumerate(result.tables):
        print(f"Table #{table_idx} has {table.row_count} rows and {table.column_count} columns")
        for cell in table.cells:
            print(f"...Cell[{cell.row_index}][{cell.column_index}]: '{cell.content}'")
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")

