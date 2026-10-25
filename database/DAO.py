from database.DB_connect import DBConnect
from model.neighbor import Neighbor
from model.state import State
from model.sighting import Sighting

class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_Lat():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct s.Lat as latitudine
                        from state s 
                        order by s.Lat ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["latitudine"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_Long():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct s.Lng as longitudine
                        from state s 
                        order by s.Lng asc;"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["longitudine"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShape():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct s.shape 
                        from sighting s 
                        order by s.shape DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getMaxMin():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT MIN(s.Lat) as minLat, MAX(s.Lat) as maxLat, MIN(s.Lng) as minLng, MAX(s.Lng)as maxLng
                    FROM state s;"""
            cursor.execute(query)

            for row in cursor:
                result.append((row["minLat"], row["minLng"], row["maxLat"], row["maxLng"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(Lat, Lng, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select s.*
                        from state s 
                        where  s.Lat >%s and s.Lng > %s 
                        and
                        EXISTS (
                            SELECT *
                            FROM sighting a
                            WHERE UPPER(a.state) = s.id
                            AND a.Shape = %s); """
            cursor.execute(query, (Lat, Lng, shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllVicini():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select n.*
                          from neighbor n 
                           """
            cursor.execute(query)

            for row in cursor:
                result.append(Neighbor(**row))
            cursor.close()
            cnx.close()
        return result







