# -*- coding: UTF-8 -*-
from loguru import logger
import mysql.connector

class MySQL:

    def connectDB(host, name, user, password, port='3306'):
        logger.info('Conectando con la base de datos')
        try:
            sql = mysql.connector.connect(
                host = host,
                port = port,
                database = name,
                user = user,
                password = password
                )
            
            logger.success('Conexión con la base de datos establecida')
            return sql
        except:
            logger.error('Error conectando a la base de datos')

            return None



