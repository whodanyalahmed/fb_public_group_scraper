url = "www.facebook.com/groups/34071880935?bac=MTUzNjU5NTgyNjoxMDE1MjQ3MTE2NTA1MDkzNjoxMDE1MjQ3MTE2NTA1MDkzNiwwLDM6MjA6S3c9PQ%3D%3D&multi_permalinks/post/asdasdasd"
#  .
raw_url = url.split('.')[1:]    
f_url = "https://www." + '.'.join(raw_url)
f_url = f_url.split('?')[0]
f_url = f_url.split('/')[2:5]

f_url = '/'.join(f_url)
print(f_url)