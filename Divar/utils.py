from typing import List

import requests


DIVAR_URL = "https://api.divar.ir/v8/web-search"


def get_ip_address(request):
    """
        Retrieve User IP Address
    """
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def single_item(data: dict) -> dict:
    """
        Cleaning Data
    """
    item = {}

    item.update(title=data["title"])
    item.update(ad_token=data["token"])
    item.update(
        images=list(map(lambda item: item["src"], data["image_url"]))
    )
    item.update(has_chat=data["has_chat"])
    item.update(is_urgent=False)

    return item


def get_items(query: str, limit: int = 24, has_photo: bool = False, urgent: bool = False, city: str = "isfahan"):
    """
        Call Divar's API
    """
    # url = DIVAR_URL + f"/{city}?q={query}"
    # if urgent:
    #     url += "&urgent=true"
    # if has_photo:
    #     url += "&has-photo=true"

    url = DIVAR_URL + f"/{city}"
    query_params = {
        "q": query,
        "has_photo": has_photo,
        "urgent": urgent,
    }

    result = []
    try:
        with requests.get(url, query_params) as response:
            print(response.url)
            # Get Only Ads
            items: List[dict] = filter(
                lambda item: item["widget_type"] == "POST_ROW",
                response.json()["web_widgets"]["post_list"]
            )

            for result_item in items:
                data: dict = result_item["data"]
                result.append(single_item(data))
    
    except Exception as error:
        print(error)

    return result[:limit]


if __name__ == "__main__":
    # _result = get_items("آپارتمان", has_photo=True)
    # print(_result[0])
    pass
