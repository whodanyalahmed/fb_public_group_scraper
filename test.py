url = "www.facebook.com/groups/34071880935?bac=MTUzNjU5NTgyNjoxMDE1MjQ3MTE2NTA1MDkzNjoxMDE1MjQ3MTE2NTA1MDkzNiwwLDM6MjA6S3c9PQ%3D%3D&multi_permalinks/post/asdasdasd"

url = url.split('.')[1:]
print(url)

init_url = "https://m."
# add init_url at index 0
url = init_url + '.'.join(url)
# remove the last part with ?
url = url.split('?')[0]

url = url.split('/')[:5]


url = '/'.join(url)

# print(url)
print(url)