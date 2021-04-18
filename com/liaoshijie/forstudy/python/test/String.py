import re

s = "12345"

print(s[1:5])

print(s[2:6])

print(s * 2)

print(s + "ABCDE")

print("----------------")
text = "<script type=\"text/javascript\">var Title=\"海贼王1010话\";var Clid=\"2\";var mhurl=\"2021/04/09221006894313.jpg\";var Url= </script>"
print(re.search("mhurl.+jpg", text).group())
match = re.match("mhurl.+jpg", text)
if match:
    print(match.group())
else:
    print("没有匹配上，兄弟")
