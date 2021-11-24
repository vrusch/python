import requests
from concurrent.futures import ThreadPoolExecutor

def post_url(args):
    return requests.post(args[0], data=args[1])
    
form_data = {
    "foo1":"bar1",
    "foo2":"bar2"
}
list_of_req = [("https://postman-echo.com/post",form_data)]*10


with ThreadPoolExecutor(max_workers=50) as pool:
    response_list = list(pool.map(post_url,list_of_req))


for response in response_list:
    print(response)