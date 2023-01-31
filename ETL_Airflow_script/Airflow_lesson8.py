import pandas as pd
import pandahouse as ph
import telegram
import io
from datetime import datetime, timedelta
from airflow.decorators import dag, task


default_args = {
    'owner': 's-dmitriev-14',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 15),
}

connection = {'host': 'https://clickhouse.lab.karpov.courses',
              'database':'simulator_20221220',
              'user':'student',
              'password':'dpo_python_2020'
              }
schedule_interval = "*/15 * * * *"

my_token = "_"
bot = telegram.Bot(token=my_token)
chat_id_group = 0

# DAG
@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)  
def dmitriev_airflow_lesson8_dag():
    
    # делаем выборку данных по ленте
    @task
    def extract_feed_actions():
        query = """
            SELECT
                toStartOfFifteenMinutes(time) as ts,
                toDate(ts) as date,
                count(distinct user_id) as users_lenta,
                countIf(action == 'view') as views,
                countIf(action == 'like') as likes,
                (countIf(action == 'like') / countIf(action = 'view')) as ctr
            FROM {db}.feed_actions
            WHERE ts >=  today() - 1 and ts < toStartOfFifteenMinutes(now())
            GROUP BY ts, date
            ORDER BY ts
            """
        df_feed_actions = ph.read_clickhouse(query=query,connection=connection)
        return df_feed_actions
    
    # делаем выборку данных по мессенджеру
    @task
    def exctract_message_actions():
        query = """
            SELECT
                toStartOfFifteenMinutes(time) as ts,
                toDate(ts) as date,
                count(distinct user_id) as users_lenta,
                count(reciever_id) as messages_sent
            FROM {db}.message_actions
            WHERE ts >=  today() - 1 and ts < toStartOfFifteenMinutes(now())
            GROUP BY ts, date
            ORDER BY ts
        """

        df_message_actions = ph.read_clickhouse(query=query,connection=connection)
        return df_message_actions
    
    #функция проверки попадания метрики в допустимый диапазон
    @task
    def metric_check(df, metric, n=5, a=5):
        df["q25"] = df[metric].shift(1).rolling(n).quantile(0.25)
        df["q75"] = df[metric].shift(1).rolling(n).quantile(0.75)
        df["iqr"] = df["q75"] - df["q25"]
        df["up"] = df["q75"] + a * df["iqr"]
        df["low"] =df["q25"] - a * df["iqr"]

        df["up"] = df["up"].rolling(n,center=True, min_periods=1).mean()
        df["low"] = df["low"].rolling(n,center=True, min_periods=1).mean()

        if df[metric].iloc[-1] < df["low"].iloc[-1] or df[metric].iloc[-1] > df["up"].iloc[-1]:
            warning = True
        else:
            warning = False
        return warning
    
    #функция проверки метрики по очереди; графики строить не будем, диапазон допустимых значений метрики мы задали достаточно большой и в случае нарушения все равно придется лезть в систему и досконально разбираться
    @task
    def check_metrics(df, metrics_list):

        for metric in metrics_list:
            tmp_df = df[['ts', 'date', metric]].copy()
            warning = metric_check(tmp_df, metric)

            if warning:
                msg = f'Метрика {metric}\nтекущее значение {tmp_df[metric].iloc[-1]:.2f}\nотклонение от предыдущего значения {abs(1- (tmp_df[metric].iloc[-1] / tmp_df[metric].iloc[-2])):.2%}\n'
                bot.sendMessage(chat_id_group, text=msg)        
    
    metrics_feed_actions = ['users_lenta','views','likes','ctr']
    metrics_message_actions = ["users_lenta","messages_sent"]
    
    df_feed_actions = extract_feed_actions()
    df_message_actions = exctract_message_actions()
    check_metrics(df_feed_actions, metrics_feed_actions)
    check_metrics(df_message_actions, metrics_message_actions)

    
sdmitriev_airflow_dag_3 = dmitriev_airflow_lesson8_dag()