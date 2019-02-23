import ast
from argparse import ArgumentParser
from pathlib import Path


global max_path_length


def conver_to_path(stack , number_list = {} ,FTT =False):
    '''

    :param stack: stack of all the visit node
    :param number_list: a uniqe id list
    :param FTT: Fot tereger the FTT model
    :return: The function return string_list that conatins the path, function_name for a function label, var_name as
    terminal node and unieqe id as copy_num
    '''
    global max_path_length
    string_list = []
    function_name = ''
    var_name = ''
    flag = False
    copy_num = number_list.copy()
    for item in stack:
        if isinstance(item, ast.FunctionDef):
            function_name = item.name
            if not(FTT):
                copy_num.remove(min(copy_num))
            flag = True
            continue
        if isinstance(item, ast.Name):
            var_name = item.id
        if not(FTT) and not(flag) and len(list(number_list)) > 1:
            copy_num.remove(min(copy_num))
        if flag:
            string = str(type(item))
            string = string.replace('<class \'_ast.','')
            string = string.replace('\'>', '')
            string_list.append(string)
    return string_list , function_name , var_name, copy_num


def dump_path_from_root_to_var(stack):
    '''
    In the case of the ftt we don't need number or more work
    :param stack: stack contains the visit node
    :return: a tupple of function name and {function_name path terminal node}
    '''
    string_list , function_name,var_name,b = conver_to_path(stack,FTT = True)
    if len(string_list) > max_path_length:
        return None,None
    string_list1 = '|'.join(string_list)
    return function_name , function_name + "," + string_list1 + "," + var_name


def check_name_item(stack , type_check):
    for item in stack:
        if isinstance(item, type_check):
            return True
    else:
        return False

var_path = dict()
global id_name
id_name = 0

def run_on_tree_FTT(node, stack):
    '''
    Simple implimation of FTT without the need of id.
    :param node: at first is the root of the tree
    :param stack: a node father stask
    '''
    global tree_syntax
    stack.append(node)
    status = True
    for child in ast.iter_child_nodes(node):
        status = False
        run_on_tree_FTT(child,stack)

    if status and check_name_item(stack,ast.Name) and check_name_item(stack,ast.FunctionDef):
        function , path  = dump_path_from_root_to_var(stack)
        if function is not None:
            if function not in tree_syntax.keys():
                tree_syntax[function] = []
            tree_syntax[function].append(path)
    stack = stack.pop(len(stack)-1)


def run_on_tree(node, stack, number_list, args, deep):
    '''
    The function creates tree_syntax. This tree_syntax includes all the path between two node of the same function.
    This function works accurding to TTT and TDT.
    :param node: at first is the root of the tree
    :param stack: a node father stask
    :param number_list: unieq id of the node
    :param args: the progrem input
    :param deep: the deep of the tree
    '''
    global id_name
    global label_list
    global tree_syntax
    global list_syntax
    id_name += 1
    stack.append(node)
    number_list.add(id_name)
    status = True
    deep += 1
    if deep > 10:
        return

    if isinstance(node, ast.FunctionDef):
        if node.name not in label_list:
            return

    for child in ast.iter_child_nodes(node):
        status = False
        run_on_tree(child, stack, number_list, args, deep)

    if status and check_name_item(stack, ast.FunctionDef) and check_name_item(stack, ast.Name):
        string_list, function, name, values = conver_to_path(stack, number_list)
        if not args.creates:
            if function not in label_list:
                stack = stack.pop(len(stack) - 1)
                number_list.remove(max(number_list))
                deep -= 1
                return

        if function not in tree_syntax.keys():
            tree_syntax[function] = []
        tree_syntax[function].append([string_list, sorted(values), name])
    stack = stack.pop(len(stack) - 1)
    number_list.remove(max(number_list))
    deep -= 1

global tree_syntax
path = dict()

def find_path():
    '''
    This function works to create the path for TTT TDT.
    :return: Create a path dictionary
    '''
    global tree_syntax
    for item in tree_syntax:
        if len(tree_syntax[item]) > 1:
            for index in range(0, len(tree_syntax[item])):
                for index1 in range(index+1, len(tree_syntax[item])):
                    set1 = set(tree_syntax[item][index][1])
                    set2 = set(tree_syntax[item][index1][1])
                    full_vector = tree_syntax[item][index][0]
                    full_vector1 = tree_syntax[item][index1][0]
                    name = tree_syntax[item][index][2]
                    name1 = tree_syntax[item][index1][2]
                    if len(sorted(set1 & set2)) > 0:
                        full_vector = full_vector[len(set1 & set2)-1:][::-1]
                        full_vector1 = full_vector1[len(set1 & set2):]
                        path_vector = full_vector + full_vector1
                        if len(path_vector)>9:
                            continue
                        if item not in path.keys():
                            path[item] = []
                        path[item].append(str(name +','+ '|'.join(path_vector)+','+ name1))


def create_data_base(file_name ,args):
    file_open = file_name.open('r',encoding = "latin-1").readlines()
    info =''.join(file_open)
    astparse = ast.parse(info)
    if args.model == 'FTT':
        run_on_tree_FTT(astparse,list())
    else:
        run_on_tree(astparse,list(),set() , args,0)
        find_path()

def convert_dic_to_extract():
    for item in path:
        print(item + " " +' '.join(path[item]))


def run_on_directory(dirctory):
    list_of_file = []
    for file in Path(dirctory).rglob('*.py'):
        if file.is_file():
            list_of_file.append(file)
    return list_of_file


if __name__ == '__main__':
    global max_path_length
    global tree_syntax
    global list_syntax
    list_syntax = list()


    max_count = 0
    parser = ArgumentParser()
    parser.add_argument("-maxlen", "--max_path_length", dest="max_path_length", required=False, default=8)
    parser.add_argument("-maxwidth", "--max_path_width", dest="max_path_width", required=False, default=2)
    parser.add_argument("-threads", "--num_threads", dest="num_threads", required=False, default=64)
    parser.add_argument("-dir", "--dir", dest="dir", required=False)
    parser.add_argument("-data", "--data", type=int, dest="data", required=False)
    parser.add_argument("-label", "--label", type=int, dest="label", required=False)
    parser.add_argument("-creates", "--creates", action='store_true', dest="creates",default=False, required=False)
    parser.add_argument("-model", "--model", dest="model", default=False, required=False)
    args = parser.parse_args()
    global label_list
    label_list = []
    if not (args.creates):
        with open('output.txt', 'r') as outfile:
            a = outfile.readlines()
            for item in a:
                label_list.append(str(item).strip('\n'))
    if args.creates:
        outfile = open('output.txt', 'w')
        outfile.close()
    list_of_file = sorted(run_on_directory(args.dir))
    max_path_length = int(args.max_path_width)
    for index in range(0,len(list_of_file)):
        item = list_of_file[index]
        try:
            tree_syntax = dict()
            create_data_base(item , args)
            if args.model=='FTT':
                path = tree_syntax
            max_count += len(path)
            if max_count > args.data:
                remove = max_count - args.data
                for i in range(0,remove):
                    path.popitem()
            convert_dic_to_extract()
            path = dict()
            if args.creates:
                outfile = open('output.txt', 'a')
                for item in tree_syntax:
                    if str(item) not in list_syntax:
                        list_syntax.append(str(item))
                        outfile.writelines(str(item) + '\n')
                outfile.close()
            if max_count >= args.data:
                break
        except SyntaxError:
            pass
        except IsADirectoryError:
            pass

