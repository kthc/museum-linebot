import os, psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', None)

class BibleDB:
    def __init__(self) -> None:
        self.con = None
        self.user_table = 'UserLog'
        self.selection_table = 'UserSelection'
    
    def connect(self, dbname="./data/longKou-market-linebot.db"):
        try:
            # self.con = sqlite3.connect(dbname, check_same_thread=False)
            self.con = psycopg2.connect(DATABASE_URL)
            return True
        except:
            return False
    
    def close(self):
        self.con.close()
    
    def create_table(self):
        cur = self.con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.user_table} (UserID VARCHAR(255), CurStoryID int, Finished int, LoginCount int, RetryCount int);""")
        self.con.commit()
        cur.close()
        print(f'{self.user_table} table created')

        cur = self.con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.selection_table} (
                UserID VARCHAR(255), 
                CurStoryID int, 
                CurrentValue VARCHAR(255),
                PRIMARY KEY (UserID, CurStoryID));""")
        self.con.commit()
        cur.close()
        print(f'{self.selection_table} table created')
    
    def drop_table(self):
        tables = [self.user_table, self.selection_table]
        for table in tables:
            cur = self.con.cursor()
            cur.execute(f"DROP TABLE {table}")
            self.con.commit()
            cur.close()
            print(f'Dropped {table} Table!')
    
    def execute(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    def get_storyid_by_userid(self, userid):
        """Get user current story id

        :param str user_id: User ID
        :return int: current story id, return 0 if not found this user id
        """
        cur = self.con.cursor()
        users = cur.execute(
        f"""SELECT CurStoryID, Finished FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        cur.close()
        if len(users) > 0:
            return users[0][0]
        else:
            print(f'UserID {userid} not found')
            return 0

    def get_finished_by_userid(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT Finished FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        cur.close()
        if len(users) > 0:
            return users[0][0] == 1
        else:
            print(f'UserID {userid} not found')
            return False

    def add_new_user(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) == 0:
            sql = f''' INSERT INTO {self.user_table} (UserID,CurStoryID,Finished,LoginCount,RetryCount)
              VALUES(%s,%s,%s,%s,%s) '''
            cur.execute(sql, (userid, 0, 0, 1,0))
            self.con.commit()
            cur.close()
            return 1
        else:
            print(f'UserID {userid} existed! Not allow to add new one')
            login_count = self.update_login_count(userid)
            return login_count

    def delete_user(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""DELETE FROM {self.user_table} WHERE UserID='{userid}'; """)
        self.con.commit()
        cur.close()

    def check_user_exist(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        cur.close()
        return len(users) > 0

    def update_login_count(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT LoginCount FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            login_count = users[0][0]
            sql = f''' UPDATE {self.user_table}
              SET LoginCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (login_count+1,userid))
            self.con.commit()
            cur.close()
            return login_count+1
        else:
            cur.close()

    def update_story_id(self, userid, storyid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = f''' UPDATE {self.user_table}
              SET CurStoryID = %s
              WHERE UserID = %s'''
            cur.execute(sql, (storyid,userid))
            self.con.commit()
        cur.close()

    def update_finished(self, userid, finished:int):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = f''' UPDATE {self.user_table}
              SET Finished = %s
              WHERE UserID = %s'''
            cur.execute(sql, (finished,userid))
            self.con.commit()
        cur.close()

    def get_retry_count_by_userid(self, userid):
        """Get retry counts for this user_id

        :param str user_id: User ID
        :return int: current retry_count, return 0 if not found this user id
        """
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT RetryCount, Finished FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        cur.close()
        if len(users) > 0:
            return users[0][0]
        else:
            print(f'UserID {userid} not found')
            return 0

    def clear_retry_count(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = f''' UPDATE {self.user_table}
              SET RetryCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (0,userid))
            self.con.commit()
        cur.close()

    def increase_1_retry_count(self, userid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.user_table} WHERE UserID='{userid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            cur_retry = self.get_retry_count_by_userid(userid)
            sql = f''' UPDATE {self.user_table}
              SET RetryCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (cur_retry+1,userid))
            self.con.commit()
        cur.close()

    def check_selection_exist(self, userid:str, storyid:int):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM {self.selection_table} WHERE UserID='{userid}' AND CurStoryID={storyid}; """)
        records = cur.fetchall()
        cur.close()
        return len(records) > 0

    def get_selection_value_by_userid_and_storyid(self, userid:str, storyid:int):
        """Get selection value for this user_id and storyid

        :param str userid: User ID
        :param str storyid: User ID
        :return str: current selection value, return None if not found
        """
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT CurrentValue FROM {self.selection_table} WHERE UserID='{userid}' AND CurStoryID={storyid}; """)
        records = cur.fetchall()
        cur.close()
        if len(records) > 0:
            return records[0][0]
        else:
            print(f'Selection Value for {userid} and {storyid} not found')
            return None

    def upsert_selection_value(self, userid:str, storyid:int, value:str):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT CurrentValue FROM {self.selection_table} WHERE UserID='{userid}' AND CurStoryID={storyid};""")
        records = cur.fetchall()
        if len(records) > 0:
            sql = f''' UPDATE {self.selection_table}
              SET CurrentValue = %s
              WHERE UserID = %s AND CurStoryID = %s'''
            cur.execute(sql, (value,userid,storyid))
            self.con.commit()
        else:
            sql = f''' INSERT INTO {self.selection_table} (UserID,CurStoryID,CurrentValue) VALUES(%s,%s,%s);'''
            cur.execute(sql, (userid, storyid, value))
            self.con.commit()
        cur.close()


def test_db():
    mydb = BibleDB()
    mydb.connect()
    mydb.create_table()
    mydb.add_new_user('ony_for_test')
    mydb.get_storyid_by_userid('ony_for_test')
    mydb.close()

db = BibleDB()
db.connect()
try:
    # db.drop_table()
    pass
except:
    pass
db.create_table()

if __name__=='__main__':
    test_db()

