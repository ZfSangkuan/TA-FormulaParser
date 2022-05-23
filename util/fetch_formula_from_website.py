import requests

r = requests.get("https://www.gupang.com/202202/60261.html")

raw_formula_str = r.text

start_pattern_str = "</div>\n\t\t\t\t\t<p>"
end_pattern_str = ";</p>"

start = raw_formula_str.index(start_pattern_str) + len(start_pattern_str)
end = raw_formula_str.index(end_pattern_str) + len(end_pattern_str)-4

raw_formula_str = raw_formula_str[start : end]

raw_formula_str = raw_formula_str.replace("<br />", " ")

start = raw_formula_str.find("<")
mid = raw_formula_str.find(">")
end = raw_formula_str.find("</a>")

while start != -1 and mid != -1 and end != -1:

    raw_formula_str = raw_formula_str[0:start] \
                    + raw_formula_str[mid+1:end].upper() \
                    + raw_formula_str[end+4: ]
    
    start = raw_formula_str.find("<")
    mid = raw_formula_str.find(">")
    end = raw_formula_str.find("</a>")

raw_formula_str = raw_formula_str.replace("&gt;", ">")
raw_formula_str = raw_formula_str.replace("&lt;", "<")

print(raw_formula_str)
