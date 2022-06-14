import mysql.connector


class MyDBInterface:
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='MusicalInstrumentsStore_copy_db'
        )
        self.cursor = self.db.cursor()

    def select_goods(self):
        self.cursor.execute('''
select g.idGood, g.Brend, g.Price, g.Model, p.Name
from Goods as g
join ProductTypes as p on (g.idProductType=p.idProductType)
order by g.idGood desc;
''')
        return list(self.cursor)

    def add_goods(self, Brand, Price, Model, ProductType):
        self.cursor.execute('''
        select idProductType 
from ProductTypes
where Name = %s;
         ''', [ProductType])
        idProductType = list(self.cursor)[0][0]
        self.cursor.execute('''
insert into Goods (Brend, Price, Model,idProductType) values
(%s, %s, %s, %s);
        ''', [Brand, Price, Model, idProductType])
        self.db.commit()

    def remove_good(self, id):
        self.cursor.execute('''
        delete from Goods
        where idGood=%s;
        ''', [id])
        self.db.commit()

    def change_good(self, id, Brand, Price, Model, ProductType):
        self.cursor.execute('''
                select idProductType 
        from ProductTypes
        where Name = %s;
                 ''', [ProductType])
        idProductType = list(self.cursor)[0][0]

        self.cursor.execute('''
        update Goods
set Brend=%s,
Price=%s,
Model=%s,
idProductType=%s
where idGood=%s;
        ''', [Brand, Price, Model, idProductType, id])
        self.db.commit()

    def can_i_add__goods(self, Brand, Model, ProductType):
        self.cursor.execute('''
                        select idProductType 
                from ProductTypes
                where Name = %s;
                         ''', [ProductType])
        idProductType = list(self.cursor)[0][0]

        self.cursor.execute('''select count(*)
                                      from Goods
                                      where Brend = %s and Model= %s 
                                      and idProductType = %s''', [Brand, Model,idProductType])
        return list(self.cursor)[0][0] == 0

    # 2 таблица

    def select_warehouses_to_goods(self):
        self.cursor.execute('''
        select w.idWarehouse, g.idGood ,concat(w.Name,': ',w.Address), concat(Brend,': ', Model,' - ',Price,'р.'), wtg.Number
            from WarehousesToGoods as wtg
                join Warehouses as w on (wtg.idWarehouse=w.idWarehouse)
                join Goods as g on (wtg.idGood=g.idGood)
            order by idWarehouse desc;
        ''')
        return list(self.cursor)

    def select_products(self):
        self.cursor.execute('''
        select  distinct  concat(Brend,': ', Model,' - ',Price,'р.') as c
                from Goods 
                order by c;
        ''')
        return [tple[0] for tple in list(self.cursor)]

    def select_warehouses(self):
        self.cursor.execute('''select distinct concat(Name,': ',Address) as c
                from Warehouses
                order by c;''')
        return [tple[0] for tple in list(self.cursor)]

    def get_warehouseId_productId(self, warehouse, product):
        self.cursor.execute('''
        select idWarehouse
            from warehouses
            where concat(Name, ': ', Address) = %s;
        ''', [warehouse])

        try:
            idWarehouse = list(self.cursor)[0][0]
        except:
            raise 'Склад не найден'

        self.cursor.execute('''
        select idGood
            from Goods 
            where concat(Brend,': ', Model,' - ',Price,'р.') = %s
            order by idGood desc;
        ''', [product])
        try:
            idGood = list(self.cursor)[0][0]
        except:
            raise 'Товар не найден'

        return [idWarehouse, idGood]

    def can_i_add_warehouse_to_goods(self, warehouse, product):
        idWarehouse, idProduct = self.get_warehouseId_productId(warehouse, product)
        self.cursor.execute('''select count(*)
                                    from warehousestogoods
                                    where idWarehouse = %s
                                    and idGood = %s''', [idWarehouse, idProduct])
        return list(self.cursor)[0][0] == 0

    def del_warehouses_to_goods(self, warehouse, product):
        idWarehouse, idProduct=self.get_warehouseId_productId(warehouse,product)
        self.cursor.execute('''
        delete from WarehousesToGoods
        where idWarehouse=%s and idGood=%s
        ''',[idWarehouse,idProduct])
        self.db.commit()

    def add_warehouses_to_goods(self, warehouse, product,number):
        idWarehouse, idProduct = self.get_warehouseId_productId(warehouse, product)
        self.cursor.execute('''
        insert into warehousestogoods (idWarehouse,idGood,Number) values
        (%s,%s,%s)
        ''',[idWarehouse,idProduct,number])
        self.db.commit()