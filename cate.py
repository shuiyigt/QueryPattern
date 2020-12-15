#coding=utf-8
import re
from collections import OrderedDict

#querys = [line.replace("<num>", "").strip().lower() for line in open("querys_8w6", encoding="utf-8")]
querys = [line.strip().lower() for line in open("robot_querys_filtered_1029", encoding="utf-8")]
querys = list(set(querys))
qlen = len(querys)
print(qlen)
#rules = [line.strip().lower() for line in open("query_rules_1214.txt", encoding="utf-8")]
rules = [line.strip().lower() for line in open("query_rules_1214_pure_cate.txt", encoding="utf-8")]

rule_querys = OrderedDict()
rules_list = list()
end_rules_list = list()
print("构建结果结构和规则结构")
for rule in rules:
    ss = rule.split("\t")
    if len(ss) < 3:
        continue
    rank, clazz, sub_clazz = int(ss[0]), ss[1], ss[2]
    if clazz not in rule_querys:
        rule_querys[clazz] = OrderedDict()
    if sub_clazz not in rule_querys[clazz]:
        rule_querys[clazz][sub_clazz] = []
    end_rules = [t.strip() for t in ss[3:] if len(t.strip()) > 0 and "$" in t] if rank < 200 else []
    if len(end_rules) > 0:
        end_rules_list.append((rank, clazz, sub_clazz, "|".join(end_rules)))
    common_rules = list(set([t.strip() for t in ss[3:] if len(t.strip()) > 0]) - set(end_rules))
    if len(common_rules) > 0:
        rules_list.append((rank, clazz, sub_clazz, "|".join(common_rules)))
    if len(end_rules) < 1 and len(common_rules) < 1:
        rules_list.append((rank, clazz, sub_clazz, ""))

#用优先级控制规则遍历顺序
end_rules_list = sorted(end_rules_list, key=lambda tup : tup[0])
rules_list = sorted(rules_list, key=lambda tup : tup[0])

print("开始找类别")
for idx, query in enumerate(querys):
    if idx % 5000 == 0:
        print(idx)
    flag = False
    for rule in end_rules_list:
        rank, clazz, sub_clazz, cur_rule = rule
        res = re.search(cur_rule, query)
        if res is None:
            continue
        (rule_querys[clazz][sub_clazz]).append((query, res.group()))
        flag = True
        break
    if flag is True:
        continue
    for rule in rules_list:
        rank, clazz, sub_clazz, cur_rule = rule
        res = re.search(cur_rule, query)
        if res is None:
            continue
        (rule_querys[clazz][sub_clazz]).append((query, res.group()))
        break

#fw = open("cate_querys", "w+", encoding="utf-8")
fw = open("cate_querys_robot", "w+", encoding="utf-8")
for clazz, d in rule_querys.items():
    for sub_clazz, qs in d.items():
        print("%s\t%s\t%s\t%s" % (clazz, sub_clazz, len(qs), round(len(qs) / qlen, 4)))
        for q, pat in qs:
            fw.write("%s\t%s\t%s\t%s\n" % (clazz, sub_clazz, q, pat))


