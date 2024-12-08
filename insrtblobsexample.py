import pymysql

connection = pymysql.connect(host='localhost', user='root', password='root', database='pds')

def insert_blob(item_desc, photo_path, color, is_new, has_pieces, material, main_cat, sub_cat):
    with connection.cursor() as cursor:
        with open(photo_path, 'rb') as file:
            binary_data = file.read()
        sql = """
        INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (item_desc, binary_data, color, is_new, has_pieces, material, main_cat, sub_cat))
        connection.commit()

insert_blob('Office Chair', '/path/to/office_chair.jpg', 'Black', True, False, 'Plastic', 'Furniture', 'Chair')
insert_blob('Dining Table', '/path/to/dining_table.jpg', 'Brown', True, False, 'Wood', 'Furniture', 'Table')

connection.close()
