import re
import string
from struct import pack,unpack
import CommandCommonProcess as ComProc
from asyncua import ua

def Convert(ArrayAddres,AddDic,flag) :
    
    #flagで処理変更
    #flag = True  →　Write

    #AddresCount = 0
    #AddresCommand = ""
    command={}
    variables ={}
    write_values = []
    #WordCount = 0
    #LongCount = 0
    
    for n in range(len(ArrayAddres)):
        if ArrayAddres[n] != "" and (AddDic[ArrayAddres[n]]['WFlag'] or not flag):

            Variable=""
            Variable = ArrayAddres[n]
            
            if AddDic[ArrayAddres[n]]['Var'] == "Short" :
                VariableType = ua.VariantType.Int16
            elif AddDic[ArrayAddres[n]]['Var'] == "UShort" :
                VariableType = ua.VariantType.UInt16
            elif AddDic[ArrayAddres[n]]['Var'] == "Long" :
                VariableType = ua.VariantType.Int32
            elif AddDic[ArrayAddres[n]]['Var'] == "ULong" :
                VariableType = ua.VariantType.UInt32
            elif AddDic[ArrayAddres[n]]['Var'] == "Float" :
                VariableType = ua.VariantType.Float

            #write_values = []
            #for name in variables.keys() :
            variables[Variable]=VariableType
            if flag :
                if AddDic[ArrayAddres[n]]['AI0'] != '' :
                    ComProc.UserToAI(AddDic,ArrayAddres[n])
                else :
                    AddDic[ArrayAddres[n]]['WAIVal'] = AddDic[ArrayAddres[n]]['WVal']
                BinaryValue=ComProc.WValueConv(ArrayAddres[n],AddDic)
                Value = ComProc.RValueConv(ArrayAddres[n],AddDic,BinaryValue)
                dv=ua.DataValue(ua.Variant(Value,VariableType))
                write_values.append(dv)



        AddDic[ArrayAddres[n]]['WFlag'] = False
    #command = list(zip(variables,write_values))
    command["Var"] = variables
    command["Val"] = write_values
    return command

def ValueGet(ArrayAddress,AddDic,Response):
    i=0
    for n in range(len(ArrayAddress)):
        if ArrayAddress[n] != '' :
            
            AddValue = Response[i]
            AddDic[ArrayAddress[n]]['RAIVal'] = AddValue
            
            if AddDic[ArrayAddress[n]]['AI0'] != '' :
                ComProc.AIToUser(AddDic,ArrayAddress[n])
            else:
                AddDic[ArrayAddress[n]]['RVal'] = AddDic[ArrayAddress[n]]['RAIVal']
                #AddDic[ArrayAddress[n]]['RhVal'] = HexValue
        i += 1


def ValueCheck(Response,ArrayAddress) :#読み込み時のnoneﾁｪｯｸ
    Result = ""
    i=0
    for Value in Response :
        if Value == None:
            Result = ArrayAddress[i]
            break
        i += 1
    
    return Result
    

def get_node(client,BefCommand,ns_index,flag) :
    command = []
    variables = BefCommand["Var"]
    write_values = BefCommand["Val"]

    nodes = [client.get_node(f"ns={ns_index};s={name}") for name in variables.keys()]

    if not flag :#読み込み
        command = nodes
    else :#書き込み
        command=list(zip(nodes,write_values))

    return command
