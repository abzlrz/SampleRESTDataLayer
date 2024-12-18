from config.db import get_db_connection

class Item:
    def __init__(self, id=None, name=None, description=None, location=None, ppu=None, uom=None, status=None):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.ppu = ppu
        self.uom = uom
        self.status = status

    @classmethod
    def add_item(cls, name, description, location, ppu, uom, status):
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
                insert into dim_items(item_name, description, location, price_per_unit, uom, status)
                values (%s, %s, %s, %s, %s, %s)
                returning item_id
        """

        cursor.execute(sql, (name, description, location, ppu, uom, status))
        
        item_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()

        return cls(id=item_id, name=name, description=description, location=location, ppu=ppu, uom=uom, status=status)

    @classmethod
    def update_item(cls, item_id, name=None, description=None, location=None, ppu=None, uom=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        update_fields = []
        update_values = []

        if name:
            update_fields.append("name = %s")
            update_values.append(name)
        if description:
            update_fields.append("description = %s")
            update_values.append(description)
        if location:
            update_fields.append("location = %s")
            update_values.append(location)
        if ppu:
            update_fields.append("ppu = %s")
            update_values.append(ppu)
        if uom:
            update_fields.append("uom = %s")
            update_values.append(uom)

        update_values.append(item_id)
        set_clause = ", ".join(update_fields)

        sql = """
                update dim_items set {set_clause}
                where item_id = %s;
        """

        cursor.execute(sql, tuple(update_values))

        conn.commit()
        cursor.close()
        conn.close()

        return cls(item_id, name, description, location, ppu, uom)