import sqlite3 as db
from pathlib import Path
from classes.dataset.normal import Normal
from classes.dataset.hmisali import Hmisali,HM_LVL
from classes.dataset.vmisali import Vmisali,VM_LVL
from classes.dataset.overhang import Overhang,OH_LVL,OH_TIPE
from classes.dataset.underhang import Underhang,UN_LVL,UN_TIPE
from classes.dataset.imbalance import Imbalance,IM_LVL
from typing import get_args
from datetime import datetime




class database_sqlite:

    def __init__(self):
        self.file_count = 0
        self.schema_path = Path(__file__).with_name("databese.sql").read_text(encoding="utf-8")

    def include_normal(self):
        with db.connect("mafaulda.db") as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self.schema_path)

            normal = Normal()
            files = normal.list_files()
            for f in files:

                file_count += 1
                time = datetime.now().strftime("%H:%M:%S")
                print(f"[{time}]add file ( {normal.get_path()} ) to database. {self.file_count}/{files.count()}")
                normal.set_file(f)

                tacometro = normal.read_tacometro()
                acel1x = normal.read_acel(1,"x").ravel()
                acel1y = normal.read_acel(1,"y").ravel()
                acel1z = normal.read_acel(1,"z").ravel()
                acel2x = normal.read_acel(2,"x").ravel() 
                acel2y = normal.read_acel(2,"y").ravel() 
                acel2z = normal.read_acel(2,"z").ravel()
                microfone = normal.read_sound()

                cursor = connection.execute(f"INSERT INTO serie (name) VALUES (\"{f}\")")
                serie_id = cursor.lastrowid

                connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 2, 0, \"normal\");") 

                indx = 1
                for s in tacometro:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                    indx += 1

                indx = 1
                for s in acel1x:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                    indx += 1
                
                indx = 1
                for s in acel1y:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                    indx += 1

                indx = 1
                for s in acel1z:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                    indx += 1

                indx = 1
                for s in acel2x:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                    indx += 1
                
                indx = 1
                for s in acel2y:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                    indx += 1

                indx = 1
                for s in acel2z:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                    indx += 1

                indx = 1
                for s in microfone:
                    connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                    indx += 1

    def insert_hmisali(self):
        with db.connect("mafaulda.db") as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self.schema_path)
            for g in get_args(HM_LVL):
                hmisali = Hmisali().set_lvl(g)
                files = hmisali.list_files()

                for f in files:
                    self.file_count += 1
                    time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{time}]add file ( {hmisali.get_path()} ) to database. {self.file_count}/{files.count()}")
                    hmisali.set_file(f)

                    tacometro = hmisali.read_tacometro()
                    acel1x = hmisali.read_acel(1,"x").ravel()
                    acel1y = hmisali.read_acel(1,"y").ravel()
                    acel1z = hmisali.read_acel(1,"z").ravel()
                    acel2x = hmisali.read_acel(2,"x").ravel() 
                    acel2y = hmisali.read_acel(2,"y").ravel() 
                    acel2z = hmisali.read_acel(2,"z").ravel()
                    microfone = hmisali.read_sound()

                    cursor = connection.execute(f"INSERT INTO serie (name) VALUES (\"{f}\")")
                    serie_id = cursor.lastrowid

                    connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 1, 0, \"falha\");") 
                    connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 8, 0, \"horizontal misalignment\");") 

                    indx = 1
                    for s in tacometro:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                        indx += 1

                    indx = 1
                    for s in acel1x:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                        indx += 1
                    
                    indx = 1
                    for s in acel1y:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                        indx += 1

                    indx = 1
                    for s in acel1z:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                        indx += 1

                    indx = 1
                    for s in acel2x:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                        indx += 1
                    
                    indx = 1
                    for s in acel2y:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                        indx += 1

                    indx = 1
                    for s in acel2z:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                        indx += 1

                    indx = 1
                    for s in microfone:
                        connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                        indx += 1

    def insert_imbalance(self):
            with db.connect("mafaulda.db") as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                connection.executescript(self.schema_path)
                for g in get_args(IM_LVL):
                    imbalance = Imbalance().set_lvl(g)
                    files = imbalance.list_files()
    
                    for f in files:
                        self.file_count += 1
                        time = datetime.now().strftime("%H:%M:%S")
                        print(f"[{time}]add file ( {imbalance.get_path()} ) to database. {self.file_count}/{files.count()}")
                        imbalance.set_file(f)
    
                        tacometro = imbalance.read_tacometro()
                        acel1x = imbalance.read_acel(1,"x").ravel()
                        acel1y = imbalance.read_acel(1,"y").ravel()
                        acel1z = imbalance.read_acel(1,"z").ravel()
                        acel2x = imbalance.read_acel(2,"x").ravel() 
                        acel2y = imbalance.read_acel(2,"y").ravel() 
                        acel2z = imbalance.read_acel(2,"z").ravel()
                        microfone = imbalance.read_sound()
    
                        cursor = connection.execute(f"INSERT INTO serie (name) VALUES (\"{f}\")")
                        serie_id = cursor.lastrowid
    
                        connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 1, 0, \"falha\");") 
                        connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 10, 0, \"imbalance\");") 
    
                        indx = 1
                        for s in tacometro:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                            indx += 1
    
                        indx = 1
                        for s in acel1x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                            indx += 1
                        
                        indx = 1
                        for s in acel1y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                            indx += 1
    
                        indx = 1
                        for s in acel1z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                            indx += 1
    
                        indx = 1
                        for s in acel2x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                            indx += 1
                        
                        indx = 1
                        for s in acel2y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                            indx += 1
    
                        indx = 1
                        for s in acel2z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                            indx += 1
    
                        indx = 1
                        for s in microfone:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                            indx += 1

    def insert_vmisali(self):
        with db.connect("mafaulda.db") as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self.schema_path)
            for g in get_args(VM_LVL):
                    vmisali = Vmisali().set_lvl(g)
                    files = vmisali.list_files()
            
                    for f in files:
                        self.file_count += 1
                        time = datetime.now().strftime("%H:%M:%S")
                        print(f"[{time}]add file ( {vmisali.get_path()} ) to database. {self.file_count}/{files.count()}")
                        vmisali.set_file(f)
            
                        tacometro = vmisali.read_tacometro()
                        acel1x = vmisali.read_acel(1,"x").ravel()
                        acel1y = vmisali.read_acel(1,"y").ravel()
                        acel1z = vmisali.read_acel(1,"z").ravel()
                        acel2x = vmisali.read_acel(2,"x").ravel() 
                        acel2y = vmisali.read_acel(2,"y").ravel() 
                        acel2z = vmisali.read_acel(2,"z").ravel()
                        microfone = vmisali.read_sound()
            
                        cursor = connection.execute(f"INSERT INTO serie (name) VALUES (\"{f}\")")
                        serie_id = cursor.lastrowid
            
                        connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 1, 0, \"falha\");") 
                        connection.execute(f"INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES({serie_id}, 9, 0, \"vertical misalignment\");") 
            
                        indx = 1
                        for s in tacometro:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                            indx += 1
            
                        indx = 1
                        for s in acel1x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                            indx += 1
                        
                        indx = 1
                        for s in acel1y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                            indx += 1
            
                        indx = 1
                        for s in acel1z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                            indx += 1
            
                        indx = 1
                        for s in acel2x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                            indx += 1
                        
                        indx = 1
                        for s in acel2y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                            indx += 1
            
                        indx = 1
                        for s in acel2z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                            indx += 1
            
                        indx = 1
                        for s in microfone:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                            indx += 1 

    def insert_overhang(self):
        condicoes_overhang = {
            "ball_fault": (4, "ball fault"),
            "cage_fault": (6, "cage fault"),
            "outer_race": (5, "outer race"),
        }
        with db.connect("mafaulda.db") as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self.schema_path)
            for tipo in get_args(OH_TIPE):
                condicao_id, descricao_condicao = condicoes_overhang[tipo]

                for g in get_args(OH_LVL):
                    overhang = Overhang().type(tipo).set_lvl(g)
                    files = overhang.list_files()

                    for f in files:
                        file_count += 1
                        time = datetime.now().strftime("%H:%M:%S")
                        print(f"[{time}]add file ( {overhang.get_path()} ) to database. {file_count}/{files.count()}")
                        overhang.set_file(f)

                        tacometro = overhang.read_tacometro()
                        acel1x = overhang.read_acel(1,"x").ravel()
                        acel1y = overhang.read_acel(1,"y").ravel()
                        acel1z = overhang.read_acel(1,"z").ravel()
                        acel2x = overhang.read_acel(2,"x").ravel()
                        acel2y = overhang.read_acel(2,"y").ravel()
                        acel2z = overhang.read_acel(2,"z").ravel()
                        microfone = overhang.read_sound()

                        cursor = connection.execute("INSERT INTO serie (name) VALUES (?)",(f,),)
                        serie_id = cursor.lastrowid

                        connection.execute("INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",(serie_id, 1, 0, "falha"),)
                        connection.execute("INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",(serie_id, condicao_id, float(g.removesuffix("g")), descricao_condicao),)
                        connection.execute("INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",(serie_id, 3, 0, 'bearing fault'),)
                        connection.execute("INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",(serie_id, 12, 0, 'outerhang'),)

                        indx = 1
                        for s in tacometro:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in microfone:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                            indx += 1

    def insert_underhang(self):
        condicoes_underhang = {
            "ball_fault": (4, "ball fault"),
            "cage_fault": (6, "cage fault"),
            "outer_race": (5, "outer race"),
        }
        with db.connect("mafaulda.db") as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(self.schema_path)
            for tipo in get_args(UN_TIPE):
                condicao_id, descricao_condicao = condicoes_underhang[tipo]

                for g in get_args(UN_LVL):
                    underhang = Underhang().tipe(tipo).set_lvl(g)
                    files = underhang.list_files()

                    for f in files:
                        file_count += 1
                        time = datetime.now().strftime("%H:%M:%S")
                        print(f"[{time}]add file ( {underhang.get_path()} ) to database. {file_count}/{files.count()}")
                        underhang.set_file(f)

                        tacometro = underhang.read_tacometro()
                        acel1x = underhang.read_acel(1,"x").ravel()
                        acel1y = underhang.read_acel(1,"y").ravel()
                        acel1z = underhang.read_acel(1,"z").ravel()
                        acel2x = underhang.read_acel(2,"x").ravel()
                        acel2y = underhang.read_acel(2,"y").ravel()
                        acel2z = underhang.read_acel(2,"z").ravel()
                        microfone = underhang.read_sound()

                        cursor = connection.execute(
                            "INSERT INTO serie (name) VALUES (?)",
                            (f,),
                        )
                        serie_id = cursor.lastrowid

                        connection.execute(
                            "INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",
                            (serie_id, 1, 0, "falha"),
                        )
                        connection.execute(
                            "INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",
                            (serie_id, condicao_id, float(g.removesuffix("g")), descricao_condicao),
                        )
                        connection.execute(
                            "INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",
                            (serie_id, 3, 0, 'bearing fault'),
                        )
                        connection.execute(
                            "INSERT INTO serie_condicao (serie, condicao, graduacao, description) VALUES (?, ?, ?, ?)",
                            (serie_id, 11, 0, 'underhang'),
                        )

                        indx = 1
                        for s in tacometro:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(1, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(2, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(3, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel1z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(4, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2x:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(5, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2y:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(6, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in acel2z:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(7, serie_id, indx, s),)
                            indx += 1

                        indx = 1
                        for s in microfone:
                            connection.execute("INSERT INTO amostras (sensor, serie, seq, value) VALUES (?, ?, ?, ?)",(8, serie_id, indx, s),)
                            indx += 1


if __name__ == "__main__":
    dbase = database_sqlite()
    dbase.insert_imbalance()