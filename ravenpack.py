from mcp.server.fastmcp import FastMCP
from typing import Any, List
from xml.etree import ElementTree as ET
from xml.dom import minidom

from bigdata_client import Bigdata
from bigdata_client.query import Similarity
from bigdata_client.models.search import SortBy
from bigdata_client.document import Document

mcp = FastMCP("RavenPack")

def convert_to_xml(documents: List[Document]) -> str:
    root_elem = ET.Element("documents")
    for doc in documents:
        document_elem = ET.SubElement(root_elem, "document")

        # Date tag
        date_elem = ET.SubElement(document_elem, "date")
        timestamp = doc.timestamp
        if timestamp:
            date_elem.text = timestamp.strftime("%Y-%m-%d")

        # Document ID tag
        doc_id_elem = ET.SubElement(document_elem, "document_id")
        doc_id_elem.text = doc.id

        # Headline tag
        headline_elem = ET.SubElement(document_elem, "headline")
        headline_elem.text = doc.headline

        # URL tag
        doc_url_elem = ET.SubElement(document_elem, "url")
        doc_url_elem.text = 'None' if doc.url is None else doc.url

        # Add chunk tags
        for chunk in doc.chunks:
            chunk_elem = ET.SubElement(document_elem, "chunk")
            # Chunk number
            chunk_num_elem = ET.SubElement(chunk_elem, "chunk_num")
            chunk_num_elem.text = str(chunk.chunk)
            # Text
            text_elem = ET.SubElement(chunk_elem, "text")
            text_elem.text = chunk.text

    # Generate string representation of the XML elements
    xml_string = ET.tostring(root_elem, encoding="unicode", method="xml")
    # Prettify the XML string
    parsed_xml_string = minidom.parseString(xml_string)
    pretty_xml_string = parsed_xml_string.toprettyxml(indent="  ")
    return pretty_xml_string

@mcp.tool()
def ravenpack(query: str) -> str:
    """
    Get bigdata content that is relevant to the user query.

    Args: 
        query: Query the user is asking
    """
    # query = "Amazon's stock price today?"
    bigdata = Bigdata(username="samuel.weller@rbccm.com", password="AidenAssist2025!")
    query = Similarity(query)
    search = bigdata.search.new(
        query,
        rerank_threshold=0.7,
        sortby=SortBy.RELEVANCE
    )
    results = search.run(limit=20)
    results_xml_string = convert_to_xml(results)
    print(results_xml_string)
    return results_xml_string


if __name__ == "__main__":
    mcp.run(transport="sse")