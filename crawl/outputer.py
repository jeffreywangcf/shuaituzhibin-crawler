import MySQLdb as mysql

class Outputer:

    def __init__(self, e, database, table):
        self.data = list()
        self.input_length = 15
        self.total_data_count = int()
        self.data_count = int()
        self.buffer_trigger = e
        self.buffer_size = 50
        self.end_writing = False
        self.order = ("名字", "国家", "星级", "图片地址", "描述", "兵种", "cost",
                     "攻击距离", "攻击", "策略", "攻城", "防御", "速度", "战法", "可拆解战法")

        with open("/Users/Excited/localmysqlrootssh.txt", "r")as f:
            local_info = f.readlines()   #host, username, passwd, port
            local_info = list(map(str.strip, local_info))
            try:
                self.connection = mysql.connect(
                    host=local_info[0],
                    user=local_info[1],
                    passwd=local_info[2],
                    db=database,
                    port=int(local_info[3]),
                    charset="utf8"
                )
            except mysql.Error as e:
                print("Error: %s" % e)
        self.cursor = self.connection.cursor()
        self.table = table

    def closeConnection(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.closeConnection()

    def collectData(self, *args):
        assert len(*args) == self.input_length
        self.data.append(tuple(*args))
        self.data_count += 1

    def exportData(self):
        while not self.end_writing:
            self.buffer_trigger.wait()
            self.addRows()
            self.data = list()
            self.total_data_count += self.data_count
            self.data_count = int()

    def getFormat(self):
        self.cursor.execute("desc %s"%self.table)
        return self.cursor.fetchall()

    def execute(self, command):
        assert isinstance(command, str)
        self.cursor.execute(command)

    def getOne(self, with_label = False):
        try:
            res = self.cursor.fetchone()
            if not with_label:
                return res
            res_dict = dict(zip([item[0] for item in self.cursor.description], res))
            return res_dict
        except mysql.Error as e:
            print("error: %s"%e)
            self.connection.rollback()
        except:
            print("error")
            self.connection.rollback()

    def getAll(self, with_label = False):
        try:
            res = self.cursor.fetchall()
            if not with_label:
                return res
            res_list = list()
            for row in res:
                res_list.append(dict(zip([item[0] for item in self.cursor.description], row)))
            return res_list
        except mysql.Error as e:
            print("error: %s"%e)
            self.connection.rollback()
        except:
            print("error")
            self.connection.rollback()

    def addRow(self, data):
        try:
            command = "insert into " + self.table + "(" + ", ".join(["`" + str(item) + "`" for item in data.keys()]) + ")"
            command += "VALUE(" + ", ".join(['"' + str(item) + '"' for item in data.values()]) +");"
            self.execute(command)
            self.connection.commit()
        except mysql.Error as e:
            print("error: %s"%e)
            self.connection.rollback()
        except:
            print("error")
            self.connection.rollback()

    def addRows(self, label = None, data = None):
        if label is None:
            label = self.order
        if data is None:
            data = self.data
        try:
            front_command = "insert into " + self.table + "(" + ", ".join(["`" + str(item).replace("\"", "") + "`" for item in label]) + ")"
            for row in data:
                self.execute(front_command + "VALUE(" + ", ".join(['"' + str(item).replace("\"", "") + '"' for item in row]) + ");")
            self.connection.commit()
        except mysql.Error as e:
            print("error: %s"%e)
            self.connection.rollback()
        except:
            print("error")
            self.connection.rollback()

    def show(self, data, length= 20, sep = " "):
        def check(item):
            if item is None:
                item = "None"
            if not isinstance(item, str):
                item = str(item)
            return item
        if isinstance(data, tuple):
            data = list(data)
        for i in range(len(data)):
            data[i] = list(map(check, data[i]))
        for line in data:
            for item in line:
                if len(item) >= length:
                    print((item[:(length-5)] + "...").center(length, sep) + "\t", end="")
                else:
                    print(item.center(length, sep) + "\t", end="")
            print()