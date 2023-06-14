import re

pattern = re.compile(r"^/[a-zA-Z]+{}png$", flags=re.DOTALL)

print(
    pattern.findall(
        "https://{s3_service}/shanyraks/507f191e810c19729de860ea/photo_1.png"
    )
)
