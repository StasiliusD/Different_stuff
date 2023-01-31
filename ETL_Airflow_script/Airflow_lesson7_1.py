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
def dmitriev_airflow_lesson7_dag():
    
    # делаем выборку дневных данных
    @task
    def daily_data():
        query = """
        SELECT toDate(time) as date,
        count(Distinct user_id) as active_users,
        sum(action = 'view') as views,
        sum(action = 'like') as likes,
        likes/views as ctr
        FROM {db}.feed_actions
        WHERE toDate(time) = yesterday()
        group by date
        """
        daily_data = ph.read_clickhouse(query, connection=connection)
        return daily_data
    
    # делаем выборку недельных данных
    @task
    def weekly_data():
        query = """
        SELECT toDate(time) as date,
        count(Distinct user_id) as active_users,
        sum(action = 'view') as views,
        sum(action = 'like') as likes,
        likes/views as ctr
        FROM {db}.feed_actions
        WHERE toDate(time) between yesterday() - 6 and yesterday()
        group by date
        """

        weekly_data = ph.read_clickhouse(query, connection=connection)
        return weekly_data
    
    #отправляем данные
    @task
    def send_daily(df1):
        bot.sendMessage(chat_id=chat_id, text = f'AU: {df1.active_users[0]}, \nViews: {df1.views[0]}, \nLikes: {df1.likes[0]}, \nCTR: {round(df1.ctr[0],3)}')
    
    #срез по полу
    @task
    def send_weekly(df2):
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle('Metrics data for previous week (Likes and CTR)', size='x-large', weight='heavy', y=1.03)

        sns.lineplot(ax = axes[0], x=df2.date, y=df2.likes).set(xlabel= None, ylabel= None)
        axes[0].set_title('Likes')

        sns.lineplot(ax = axes[1], x=df2.date, y=df2.ctr).set(xlabel= None, ylabel= None)
        axes[1].set_title('CTR')

        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'plotline.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle('Metrics data for previous week (AU and Views)', size='x-large', weight='heavy', y=1.03)

        sns.lineplot(ax = axes[0], x=df2.date, y=df2.active_users).set(xlabel= None, ylabel= None)
        axes[0].set_title('Active_users')

        sns.lineplot(ax = axes[1], x=df2.date, y=df2.views).set(xlabel= None, ylabel= None)
        axes[1].set_title('Views')

        plot_object = io.BytesIO()
        plt.savefig(plot_object)
        plot_object.seek(0)
        plot_object.name = 'plotline.png'
        plt.close()
        bot.sendPhoto(chat_id=chat_id, photo=plot_object)        
    
    daily_data = daily_data()
    weekly_data = weekly_data()
    send_daily(daily_data)
    send_weekly(weekly_data)

    
sdmitriev_airflow_dag_2 = dmitriev_airflow_lesson7_dag()