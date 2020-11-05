import mysql.connector
import json

mydb = mysql.connector.connect(
    host="vps-45d5666d.vps.ovh.net",
    user="teamUser",
    password="ArtxSROmit345@",
    database="GREENOVERFLOW"
)

TABLE_INR = "INR_SCORE_GLOBAL"
TABLE_ZIP = "CORRELATION_CODE_INSEE_POSTAL"
TABLE_DPT = "DEPARTEMENT_CODE_NAME"
TABLE_REG = "REGION_CODE_NAME"
mycursor = mydb.cursor()


def list_strjoin(l, pre='', post='', sep=', '):
    res = str()
    for e in l:
        res += str(pre)
        res += str(e)
        res += str(post)
        res += str(sep)
    return res[:-len(sep)]


def optional_map(f, l):
    return map(lambda x: None if x is None else f(x), l)


def avg_test(cursor, commune_name, columns):
    avgcolnames = list_strjoin(columns, 'AVG(', ')')
    cursor.execute(f"""
                   SELECT commune_name, {avgcolnames}
                   FROM {TABLE_INR}
                   WHERE commune_name = '{commune_name}'
                   """)
    result = cursor.fetchall()[0]
    averages = dict(zip(columns, result[1:]))
    return result[0], averages


def avg_city(cursor, postal_code, columns):
    avgcolnames = list_strjoin(columns, 'AVG(', ')')
    cursor.execute(f"""
                   SELECT commune_name, {avgcolnames}
                   FROM {TABLE_INR}
                       INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
                   WHERE postal_code = '{postal_code}'
                   """)
    result = cursor.fetchall()[0]
    averages = dict(zip(columns, optional_map(float, result[1:])))
    return {'name': result[0], 'averages': averages}


def avg_dpt(cursor, postal_code, columns):
    avgcolnames = list_strjoin(columns, 'AVG(', ')')
    cursor.execute(f"""
                    SELECT departement_name, {avgcolnames}
                    FROM {TABLE_INR}
                        INNER JOIN {TABLE_ZIP} ON {TABLE_INR}.insee_code = {TABLE_ZIP}.insee_code
                        INNER JOIN {TABLE_DPT} ON {TABLE_INR}.departement_code = {TABLE_DPT}.departement_code
                    WHERE {TABLE_INR}.departement_code IN (SELECT departement_code
                                                           FROM {TABLE_INR} INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
                                                           WHERE postal_code = '{postal_code}')
                    """)
    result = cursor.fetchall()[0]
    averages = dict(zip(columns, optional_map(float, result[1:])))
    return {'name': result[0], 'averages': averages}


def avg_reg(cursor, postal_code, columns):
    avgcolnames = list_strjoin(columns, 'AVG(', ')')
    cursor.execute(f"""
                    SELECT region_name, {avgcolnames}
                    FROM {TABLE_INR}
                        INNER JOIN {TABLE_ZIP} ON {TABLE_INR}.insee_code = {TABLE_ZIP}.insee_code
                        INNER JOIN {TABLE_REG} ON {TABLE_INR}.region_code = {TABLE_REG}.region_code
                    WHERE {TABLE_INR}.region_code IN (SELECT region_code
                                                           FROM {TABLE_INR} INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
                                                           WHERE postal_code = '{postal_code}')
                    """)
    result = cursor.fetchall()[0]
    averages = dict(zip(columns, optional_map(float, result[1:])))
    return {'name': result[0], 'averages': averages}


def indexes(postal_code):
    postal_code = str(postal_code)
    mycursor = mydb.cursor()
    columns = ['GLOBAL_SCORE', 'DIGITAL_UI_ACCESS', 'INFORMATION_ACCESS', 'ADMINISTRATIVE_SKILLS',
               'DIGITAL_ACADEMIC_SKILLS']
    city = avg_city(mycursor, postal_code, columns)
    dpt = avg_dpt(mycursor, postal_code, ['GLOBAL_SCORE'])
    reg = avg_reg(mycursor, postal_code, ['GLOBAL_SCORE'])
    return {'city': city, 'departement': dpt, 'region': reg}


def to_api(dct):
    try:
        api_dct = {
            "communeName": str(dct["city"]["name"]),
            "global": int(dct["city"]["averages"]["GLOBAL_SCORE"]),
            "region": int(dct["region"]['averages']["GLOBAL_SCORE"]),
            "regionName": str(dct["region"]["name"]),
            "departement": int(dct["departement"]['averages']["GLOBAL_SCORE"]),
            "departementName": str(dct["departement"]["name"]),
            "digitalInterfaceAccess": int(dct["city"]['averages']["DIGITAL_UI_ACCESS"]),
            "informationAccess": int(dct["city"]['averages']["INFORMATION_ACCESS"]),
            "administrativeCompetences": int(dct["city"]['averages']["ADMINISTRATIVE_SKILLS"]),
            "digitalAndScolarCompetences": int(dct["city"]['averages']["DIGITAL_ACADEMIC_SKILLS"]),
        }
    except (KeyError, TypeError):
        return None

    return api_dct


# ne marche pas pour l'instant
def single(postal_code):
    postal_code = str(postal_code)
    mycursor = mydb.cursor()
    columns = ['GLOBAL_SCORE', 'DIGITAL_UI_ACCESS', 'INFORMATION_ACCESS', 'ADMINISTRATIVE_SKILLS',
               'DIGITAL_ACADEMIC_SKILLS']
    avgcolnames = list_strjoin(columns, 'AVG(', ')')
    mycursor.execute(f"""
    SELECT
        (SELECT commune_name, {avgcolnames}
         FROM {TABLE_INR}
             INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
         WHERE postal_code = '{postal_code}'
        ),
        (SELECT departement_name, AVG(GLOBAL_SCORE)
         FROM {TABLE_INR}
             INNER JOIN {TABLE_ZIP} ON {TABLE_INR}.insee_code = {TABLE_ZIP}.insee_code
             INNER JOIN {TABLE_DPT} ON {TABLE_INR}.departement_code = {TABLE_DPT}.departement_code
         WHERE {TABLE_INR}.departement_code IN (SELECT departement_code
                                                FROM {TABLE_INR} INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
                                                WHERE postal_code = '{postal_code}')
        ),
        (SELECT region_name, AVG(GLOBAL_SCORE)
         FROM {TABLE_INR}
             INNER JOIN {TABLE_ZIP} ON {TABLE_INR}.insee_code = {TABLE_ZIP}.insee_code
             INNER JOIN {TABLE_REG} ON {TABLE_INR}.region_code = {TABLE_REG}.region_code
         WHERE {TABLE_INR}.region_code IN (SELECT region_code
                                                FROM {TABLE_INR} INNER JOIN {TABLE_ZIP} ON {TABLE_ZIP}.insee_code = {TABLE_INR}.insee_code
                                                WHERE postal_code = '{postal_code}')
        )
    """)
    return mycursor.fetchall()
