import re

pattern = re.compile(r"")

input = "https://s3-eu-central-1.amazonaws.com/dattebayokz-bucket/images/pexels-james-wheeler-417074.jpg"

strs = input.split("/")

print(strs[-1])
# print(
#     pattern.findall(
#         "https://s3-eu-central-1.amazonaws.com/dattebayokz-bucket/images/pexels-james-wheeler-417074.jpg"
#     )
# )
