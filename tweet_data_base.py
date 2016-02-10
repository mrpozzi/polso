__author__ = 'mrpozzi'


import MySQLdb

# Open database connection
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="luca", # your username
                     passwd="", # your password
                     db="twitterdb") # name of the data base


if __name__ == '__main__':

    """
    For this function to be used you need to install mysql then
    start the server with the command:
    sudo /usr/local/bin/mysql.server restart
    (the path depends on your installation
    /usr/local/Cellar/mysql/5.6.22/bin/mysql.server
    /usr/local/Cellar/mysql/5.6.22/support-files/mysql.server start
    with brew install.)

    Also before update /usr/local/Cellar/mysql/5.6.22/my.cnf
    with:

    [mysqld]
    pid-file = /usr/local/var/mysql/Lucas-Air.attlocal.net.pid

    Then you need to configure the user and create the database

    mysql --user=root mysql
    CREATE USER 'luca'@'localhost';
    GRANT ALL PRIVILEGES ON *.* TO 'luca'@'localhost' WITH GRANT OPTION;
    CREATE SCHEMA twitterdb;

    """

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Drop table if it already exist using execute() method.
    #cursor.execute("DROP TABLE IF EXISTS TRENDS")

    # Create table as per requirement
    sql = """CREATE TABLE TRENDS (
        DATE  CHAR(20) NOT NULL,
        LOCATION  CHAR(200) NOT NULL,
        JSON TEXT)"""

    cursor.execute(sql)