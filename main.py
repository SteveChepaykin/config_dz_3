import xml.etree.ElementTree as ET

functions = {
    "+": lambda a, b: a+b,
    "-": lambda a, b: a-b,
    "/": lambda a, b: a/b,
    "*": lambda a, b: a*b,
    "len": lambda a: len(a),
    "ord": lambda a, b: a.find(b) 
}

variables = {}

def parseXmlToConfig(xml_data):
    try:
        root = ET.parse(xml_data)
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return

    output_lines = []

    for comment in root.findall("comment"):
        comment_text = comment.text.strip()
        output_lines.append(f"{{{{!--\n{comment_text}\n}}}}")

    for array in root.findall("array"):
        values = [v.text for v in array.findall("value")]
        output_lines.append(f"[ {'; '.join(values)} ]")
    
    for constant in root.findall("constant"):
        name = constant.get("name")
        value = constant.text.strip()
        output_lines.append(f"var {name} := {value};")

    for expression in root.findall("expression"):
        val1 = expression.get("value1")
        val2 = expression.get("value2")
        oper = expression.get("operation")
        output_lines.append(f"?{{{val1} {oper} {val2}}}")

    outf = open(f"{(xml_data.split('.')[0])}.txt", 'w');
    for line in output_lines:
        outf.write(line+"\n")
    outf.close()

def processConfig(name):
    global functions;
    global variables;
    inComment = False;
    inf = open(f"{name}.txt", 'r')
    outf = open("log.txt", 'w')

    for line in inf.readlines():
        if line == "": continue
        elif inComment and line == "}}\n":
            inComment = False
            continue
        elif line.startswith("{{!--"):
            inComment = True
            continue
        elif inComment: continue
        elif line.startswith("var"):
            temp = line[4:-1].split(" := ")
            name = temp[0]
            value = temp[1][:-1]
            if(value.startswith("q(")):
                value = str(value[3:-1])
            else:
                value = int(value)
            variables[name] = value
            outf.write("added value " + str(value) + " as " + str(name) + "\n")
        elif line.startswith("["):
            temp = line[2:-3].split("; ")
            counter = 0;
            for i in variables:
                if i is list: counter+=1
            name = "array"+str(counter)
            variables[name] = temp
            outf.write("added list " + line[2:-2] + " as " + name + "\n")
        elif line.startswith("?{"):
            temp = line[2:-2].split(" ")
            if len(temp) != 3:
                if len(temp) == 1:
                    if temp[0].startswith("len("):
                        temp = temp[0][4:-1]

                    elif temp[0].startswith("ord("):
                        temp = temp[0][4:-1]

                else:
                    outf.write("incorrect expression\n")
                    continue
            else:
                val1 = temp[0]
                oper = temp[1]
                val2 = temp[2]
                nval1, nval2 = 0, 0
                fromvar = False
                if(val1 in variables.keys()):
                    nval1 = variables[val1]
                    fromvar = True
                else: nval1 = val1
                if(val2 in variables.keys()):
                    nval2 = variables[val2]
                else: nval2 = val2
                res = functions[oper](int(nval1), int(nval2))
                if fromvar:
                    variables[val1] = res
                    outf.write("new value of " + str(val1) + " : " + str(variables[val1]))
                else:
                    outf.write(val1 + " " + oper + " " + val2 + " = " + str(res) + "\n")
    
    inf.close()
    outf.close()
        
if __name__ == "__main__":
    n = str(input("enter XML file name (with extension): "))
    on = n.split(".")[0]
    parseXmlToConfig(n)
    processConfig(on)
