import mariadb
import pandas as pd
import sys
import logging
import os
from config import db_usr, db_pwd, db_host, db_name, db_port

filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'meme_app.log')
logging.basicConfig(filename=filename, filemode='a', level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():

    try:
    
        logging.info('Getting meme data.')
        
        conn = mariadb.connect(
                user=db_usr,
                password=db_pwd,
                host=db_host,
                port=db_port,
                database=db_name)
        cur = conn.cursor() 
        
        #retrieving information 
        
        cur.execute(
        """
        WITH TEMP AS(
        SELECT
            CAST(DT AS DATE) DT,
            CASE
                WHEN CLASSIFICATION = 0
                THEN 1
                ELSE 0
            END AS PEPE,
            CASE
                WHEN CLASSIFICATION = 1
                THEN 1
                ELSE 0
            END AS BOBO,
            CASE
                WHEN CLASSIFICATION = 2
                THEN 1
                ELSE 0
            END AS OTHER
        FROM BIZ_HISTORY)

        SELECT
            CAST(DT AS DATE) DT,
            sum(PEPE) / sum(BOBO) PEPE_RATIO,
            sum(OTHER) OTHER_SUM,
            COUNT(*) COUNT
        FROM TEMP
        GROUP BY CAST(DT AS DATE)
        HAVING CAST(DT AS DATE) >= '2022-02-15' -- AND COUNT > 1000
        ORDER BY CAST(DT AS DATE) ASC
        ;
        """    
        )
        
        dts = []
        pepe_ratios = []
        for row in cur:
            dts.append(row[0])
            pepe_ratios.append(float(row[1]))
            
        conn.close()
        
        dict = {'time': dts, 'pepe_ratio': pepe_ratios} 
        df = pd.DataFrame(dict)
        df.rename(columns={'pepe_ratio': 'value'}, inplace=True)
        df['time'] = pd.to_datetime(df['time'])
        df['time'] = df['time'].values.astype(float)/1000000000
        df['time'] = df['time'].astype(int)
        df.to_csv('/app/misc_files/pepe_ratio.csv', index=False)
        logging.info('Meme data successfully saved.')
        
    except Exception as e:
    
        logging.error(f'Could not save meme data: {e}')

if __name__ == '__main__':
    
    main()