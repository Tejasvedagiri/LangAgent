from typing import Any
import requests

def remove_empty_values(content):
    keys_to_delete = []
    for key, value in content.items():
        if not value or ((isinstance(value, str) or isinstance(value, list) or isinstance(value, dict))and len(value) == 0):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del content[key]
    return content

def scrape_linked_url(api_url:str) -> dict[str, Any]:
    """
    Something something doc strings allow langchain to use
    :return:
    """

    res = requests.get(api_url)
    if res.status_code == 200:
        data = res.json()
        content = {
            "person" : remove_empty_values(data["person"]),
            "company": remove_empty_values(data["company"])
        }
        return content
    else:
        raise Exception("Failed to pull LinkedIn details")

if __name__=="__main__":
    print(scrape_linked_url("https://gist.githubusercontent.com/Tejasvedagiri/c3c850af20fe6714f09ea9173b28c684/raw/aab98931a95cdfe05bfd2e300f9d995446d3def2/tejas_vedagiri_linked_in"))