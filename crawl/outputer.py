import MySQLdb as mysql

class Outputer:

    def __init__(self, database, table):
        self.name = list()
        self.country = list()
        self.star = list()
        self.image_address = list()
        self.description = list()
        self.kind = list()
        self.cost = list()
        self.attack_range = list()
        self.attack = list()
        self.ruse = list()
        self.seige = list()
        self.defand = list()
        self.speed = list()
        self.carry_skill = list()
        self.decomposable_skill = list()
        self.input_length = 15

        with open("/Users/Excited/localmysqlrootssh.txt", "r")as f:
            local_info = f.readlines()   #host, username, passwd, port
            try:
                self.connection = mysql.connect(
                    host=local_info[0],
                    user=local_info[1],
                    passwd=local_info[2],
                    db=database,
                    port=local_info[3],
                    charset="utf8"
                )
            except mysql.Error as e:
                print("Error: %s" % e)
        self.cursor = self.connection.cursor()
        self.table = table

    def __del__(self):
        self.closeConnection()

    def closeConnection(self):
        if self.connection:
            self.connection.close()

    def collectData(self, *args):
        assert len(*args) == self.input_length
        self.name.append(*args[0])
        self.country.append(*args[1])
        self.star.append(*args[2])
        self.image_address.append(*args[3])
        self.description.append(*args[4])
        self.kind.append(*args[5])
        self.cost.append(*args[6])
        self.attack_range.append(*args[7])
        self.attack.append(*args[8])
        self.ruse.append(*args[9])
        self.seige.append(*args[10])
        self.defand.append(*args[11])
        self.speed.append(*args[12])
        self.carry_skill.append(*args[13])
        self.decomposable_skill.append(*args[14])

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

    def addRows(self, label, data):
        try:
            front_command = "insert into " + self.table + "(" + ", ".join(["`" + str(item) + "`" for item in label]) + ")"
            for row in data:
                self.execute(front_command + "VALUE(" + ", ".join(['"' + str(item) + '"' for item in row]) + ");")
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