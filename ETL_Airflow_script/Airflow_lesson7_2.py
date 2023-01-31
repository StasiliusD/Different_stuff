# coding=utf-8

import pandas as pd
import pandahouse as ph
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import telegram
import io
from airflow.decorators import dag, task
from datetime import timedelta, datetime

connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'database': 'simulator_20221220',
    'user': 'student',
    'password': 'dpo_python_2020'
}

default_args = {
    'owner': 's-dmitriev-14',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 12)
}

# Интервал запуска DAG
schedule_interval = '0 11 * * *'

token = '5880452781:AAEvY1EqwaUv_4Eo1TiPz0RLf-35IhWEvk8'
bot = telegram.Bot(token=token)
chat_id = 1231933628

# DAG
@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)  
def dmitriev_airflow_lesson7_dag2():
    
    # делаем выборку данных
    @task
    def extract_data():
        query = """
        SELECT toDate(time) as date,
        countIf(Distinct user_id, "reciever_id" = 0) as only_news_users,
        countIf(Distinct user_id, "reciever_id" != 0) as news_message_users,
        round(sum(action = 'like')/sum(action = 'view'),3) as ctr,
        round(news_message_users/only_news_users,3) as messenger_usage_rate
        from
        (select user_id, action, time from {db}.feed_actions) t1
        left join
        (select user_id, time, reciever_id from {db}.message_actions) t2
        using user_id

        WHERE toDate(time) between yesterday() - 30 and yesterday()
        group by date
        """
        data = ph.read_clickhouse(query, connection=connection)
        return data

    #отправляем данные
    @task
    def send_first_package(df1):
        news_message_users_yesterday = df1.news_message_users.iloc[-1]
        users_only_news_yesterday = df1.only_news_users.iloc[-1]
        ctr_yesterday = df1.ctr.iloc[-1]
        
        bot.sendMessage(chat_id=chat_id, text = f'Пользователи (новости+мессенджер) вчера: {news_message_users_yesterday}, \nПользователи (новости) вчера: {users_only_news_yesterday}, \nCTR вчера: {ctr_yesterday}, \nMessenger_usage_rate вчера: {messenger_usage_rate}')
    
    @task
    def send_second_package(df1):        
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle('Audience metrics', size='x-large', weight='heavy', y=1.03)

        sns.lineplot(ax = axes[0], x=df1.date, y=df1.only_news_users).set(xlabel= None, ylabel= None)
        axes[0].set_title('Only_news_users')

        sns.lineplot(ax = axes[1], x=df1.date, y=df1.news_message_users).set(xlabel= None, ylabel= None)
        axes[1].set_title('News_message_users')

        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'plotline.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle('CTR and Messenger usage rate', size='x-large', weight='heavy', y=1.03)

        sns.lineplot(ax = axes[0], x=df1.date, y=df1.ctr).set(xlabel= None, ylabel= None)
        axes[0].set_title('CTR')

        sns.lineplot(ax = axes[1], x=df1.date, y=df1.messenger_usage_rate).set(xlabel= None, ylabel= None)
        axes[1].set_title('Messenger_usage_rate')

        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'plotline.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)    
 
    data = extract_data()
    send_first_package(data)
    send_second_package(data)
    
sdmitriev_airflow_dag_3 = dmitriev_airflow_lesson7_dag2()