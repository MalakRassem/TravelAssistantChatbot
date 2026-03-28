import requests
from fastmcp import FastMCP
import os

mcp = FastMCP("ServerB")


#    https://api.openalex.org/works ([OpenAlex](https://docs.openalex.org/api-entities/works/search-works))


@mcp.tool
def wikiextract(topic: str):
    payload = {'action': "query",
               'prop': "extracts",
               'titles': topic,
               'exintro': True,
               'explaintext': True,
               'redirects': True,
               'format': "json"
               }

    headers = {"User-Agent": "TravelAssistantChatbot"}
    wikipedia_url = "https://en.wikipedia.org/w/api.php"
    response = requests.get(wikipedia_url, params=payload, headers=headers)
    if response.status_code == 200:
        try:
            return list(response.json()['query']['pages'].values())[0]["extract"]
        except:
            print("Response received from API call has unexpected structure.",
                  response.json())  # TODO: Exception Handling
    else:
        # TODO: Exception Handling
        print(f"API Request Failed. Status Code: {response.status_code}")


@mcp.tool
def openalexsearchworks(query: str, other_params: dict = {}):
    """
    Query the OpenAlex API for scholarly references relevant to a user's question.

    The API key is included automatically in the request parameters. The `query`
    argument is used as the value of the API's search parameter. Additional
    parameters may be supplied through `other_params`, as long as they are valid
    according to the OpenAlex API documentation.

    The returned reference should contain enough information to answer the user's
    question.

    Args:
        query (str): The search string to send to the OpenAlex API as the search parameter's value.
        other_params (dict, optional): Additional API parameters to refine the
            request.

    Returns:
        str: A JSON-formatted string containing the API response.
    """
    payload = {'api_key': os.environ.get("OPENALEX_API_KEY"),
               'search': query,
               }
    payload.update(other_params)
    openalex_url = "https://api.openalex.org/works"
    response = requests.get(openalex_url, params=payload)
    if response.status_code == 200:
        try:
            return response.json()["results"]
        except:
            print("Response received from API call has unexpected structure.",
                  response.json())  # TODO: Exception Handling
    else:
        # TODO: Exception Handling
        print(f"API Request Failed. Status Code: {response.status_code}")


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001)
