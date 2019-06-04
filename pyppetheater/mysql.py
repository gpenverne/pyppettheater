import pymysql

class Actor():

    def __init__(self, parameters):
       self.db = pymysql.connect(
           host=parameters['mysql']['db_host'],
           user=parameters['mysql']['db_user'],
           passwd=parameters['mysql']['db_password'],
           db=parameters['mysql']['db_name']
       )

    # Then the row with ":key" equal to ":value" in table ":table:" should exist
    async def the_row_with_equal_to_in_table_should_exist(self, row_key, row_value, table_name):
        cur = self.db.cursor()
        cur.execute('SELECT id FROM '+table_name+' WHERE '+row_key+'="'+row_value+'"')
        for row in cur.fetchall():
            return True
        raise Exception ('No row with '+row_key+' equal to '+row_value+' found in table '+table_name)

    # Then the row with ":key" equal to ":value" in table ":table:" should not exist
    async def the_row_with_equal_to_in_table_should_not_exist(self, row_key, row_value, table_name):
        cur = self.db.cursor()
        cur.execute('SELECT id FROM '+table_name+' WHERE '+row_key+'="'+row_value+'"')
        for row in cur.fetchall():
            raise Exception ('A row with '+row_key+' equal to '+row_value+' has been found in table '+table_name+', but it should not.')
        return True

    # Given the row with ":key" equal to ":value" in table ":table:" has ":other_key" equal to ":new_value"
    async def the_row_with_equal_to_in_table_has_equal_to(self, row_key, row_value, table_name, other_key, new_value):
        cur = self.db.cursor()
        cur.execute('UPDATE '+table_name+' SET '+other_key+' = "' + new_value + '" WHERE '+row_key+'="'+row_value+'"')
        self.db.commit()

    # Given the row with ":key" equal to ":value" in table ":table:" does not exist
    async def the_row_with_equal_to_in_table_does_not_exist(self, row_key, row_value, table_name):
        cur = self.db.cursor()
        cur.execute('DELETE FROM '+table_name+' WHERE '+row_key+'="'+row_value+'"')
        self.db.commit()

    # Then the row with ":key" equal to ":value" in table ":table:" should have ":other_key" equal to ":new_value"
    async def the_row_with_equal_to_in_table_should_have_equal_to(self, row_key, row_value, table_name, other_key, new_value):
        cur = self.db.cursor()
        cur.execute('SELECT '+other_key+' FROM '+table_name+' WHERE '+row_key+'="'+row_value+'"')
        for row in cur.fetchall():
            if row[0] == new_value:
                return True

            raise Exception ('The row with '+row_key+' equal to '+row_value+' has '+row[0]+' as value, '+new_value+' was expected.')
        return True
