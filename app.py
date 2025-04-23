import cohere
from fastapi import FastAPI
from bigdata_client import Bigdata
from bigdata_client.query import Similarity
from bigdata_client.models.search import SortBy
from bigdata_client.document import Document
import nest_asyncio
import uvicorn
from ravenpack import convert_to_xml

app = FastAPI()

DISABLE_NEST_ASYNCIO=True

@app.post("/slides_prompt")
def slides_system_prompt(user_input):
    co = cohere.ClientV2(api_key="kfSIAfOx2Cz2NvUoF9DkqVAkEnBVrdnBYYHUTAgG")

    system_message = """
    ## Task And Context
1. Use the marp tool for this function to generate a markdown. 
2. Generate images e.g. for less than half of the slides. Add a title slide
3. Give longer paragraphs less than half of the time and include more bullet points
4. Your name is North! You are an internal knowledge assistant for the company Cohere. 
5. You use your advanced complex reasoning capabilities to help people by answering their questions and other requests interactively. 
6. You will be asked a very wide array of requests on all kinds of topics. 
7. You will be equipped with a wide range of search engines or similar tools to help you, which you use to research your answer. 
8. You may need to use multiple tools in parallel or sequentially to complete your task. 
9. You should focus on serving the user's needs as best you can, which will be wide-ranging. 
10. You are an expert on every company topic. Explain your reasoning step by step. 
11. Add nuance to your answer, by taking a step back: how confident are you about the answer? Any caveats? Does it seem weird or against common sense?

## Style Guide
1. Ensure the content fits the slide. 
2. Use paragraphs and long format content and fewer bullet points.
3. Create the powerpoint without giving the user extra information about the powerpoint creation.
4. Remove the last slide saying who created it.
5. Unless the user asks for a different style of answer, you should answer in full sentences, using proper grammar and spelling. 
    """

    res = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    final_result = (res.message.content[0].text)
    print(final_result)
    return final_result


@app.post("/ravenpack")
def ravenpack(query: str) -> str:
    """
    Get bigdata content that is relevant to the user query.

    Args: 
        query: Query the user is asking
    """
    
    bigdata = Bigdata(username="samuel.weller@rbccm.com", password="AidenAssist2025!")
    query = Similarity(query)
    search = bigdata.search.new(
        query,
        rerank_threshold=0.7,
        sortby=SortBy.RELEVANCE
    )
    results = search.run(limit=20)
    results_xml_string = convert_to_xml(results)
    return results_xml_string


if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run("app:app", host="0.0.0.0", port=8080, workers = 2, log_level="info", loop='asyncio')
    #  mcp.run(transport="sse")