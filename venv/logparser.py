import re

txt = open('kernlog.txt', 'r')
csv = open('kernlog.csv', 'w')
regex_num = re.compile('\d+[.]?\d*')

for line in txt:
    s = ','.join(regex_num.findall(line)) + '\n'
    csv.write(s)

