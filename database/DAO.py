from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    @staticmethod
    def get_all_anni():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ select distinct YEAR(s.`datetime`) as year
                    from sighting s 
                    where 1910 <= YEAR(s.`datetime`) <= 2014 """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def get_forme_anno(anno):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ select distinct s.shape
                    from sighting s
                    where year(s.`datetime`) = %s 
                    and s.shape != "" """

        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def get_nodi():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """ select distinct s.* 
                from state s """

        cursor.execute(query)
        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        cnx.close()

        return result



    @staticmethod
    def get_archi(anno, forma, idMap_nodi):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []

        query = """SELECT n.state1, n.state2 , count(*) as N
                            FROM sighting s , neighbor n 
                            where year(s.`datetime`) = %s
                            and s.shape = %s
                            and (s.state = n.state1 or s.state = n.state2 )
                            and n.state1 < n.state2
                            group by n.state1 , n.state2 """

        cursor.execute(query, (anno, forma))

        for row in cursor:
            s1 = idMap_nodi[row['state1']]
            s2 = idMap_nodi[row['state2']]
            result.append((s1, s2, row["N"]))

        cursor.close()
        cnx.close()

        return result