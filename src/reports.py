import pandas as pd
import logging
import datetime

# json  # pytest
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/src.reports.log", mode="w")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


file_path = 'C:/Users/Helen/PycharmProjects/Project_1_Bank/data/operations.xlsx'
df = pd.read_excel(file_path)


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: str | None = None) -> pd.DataFrame:

    new_df = transactions[transactions['Категория'] == category]
    if date is None:
        date_now = datetime.datetime.now()
        date = datetime.datetime.strftime(date_now, '%d.%m.%Y %H:%M:%S')

    new_df['Дата операции'] = new_df['Дата операции'].astype('datetime64[ns]')
    new_df['year_month'] = new_df['Дата операции'].dt.to_period("M")



    #date_2 =
    #new_df_sort_data = new_df[new_df['Дата операции'] > (lambda x: )]


    month = date.month - 2
    def aaa():




    return new_df

if __name__ == "__main__":
    print(spending_by_category(df,'Фастфуд'))