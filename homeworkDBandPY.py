import psycopg2
from pprint import pprint

print("""
Добро пожаловать в программу для управления клиентами! 
\nПожалуйста,введите необходимую команду из предложенного списка, 
а затем выполните необходимое Вам действие
\nДля создания структуры БД (таблицы) введите  0
Для добавления нового клиента введите  1
Для добавления телефона для существующего клиента введите  2
Для изменения имени клиента введите  3
Для изменения фамилии клиента введите  4
Для изменения e-mail клиента введите  5
Для изменения номера телефона клиента введите  6
Для удаления номера телефона существующего клиента введите  7
Для удаления существующего клиента введите  8
Для поиска существующего клиента по его данным введите  9""")


conn = psycopg2.connect(user="postgres", password="pwd", database="pywork", port="5432")


def create_tables():
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_Homework5(
        id SERIAL PRIMARY KEY, 
        client_name VARCHAR(100) NOT NULL, 
        client_surname VARCHAR(100) NOT NULL, 
        client_email VARCHAR(100) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_phonenumbers(
        id_phonenumber SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients_Homework5(id),
        client_phonenumber INTEGER UNIQUE);
        """)
        conn.commit()


def add_new_client():
    input_client_name = input("Введите имя клиента для добавления в таблицу: ")
    input_client_surname = input("Введите фамилию клиента для добавления в таблицу: ")
    input_client_email = input("Введите email клиента для добавления в таблицу: ")
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients_Homework5(client_name, client_surname, client_email) VALUES(%s, %s, %s);
        """, (input_client_name, input_client_surname, input_client_email))
        conn.commit()



def add_new_phonenumber():
    input_client_id = input("Введите id клиента для добавления номера телефона: ")
    input_phonenumber = input("Введите номер телефона для добавления: ")
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client_phonenumbers(client_id, client_phonenumber) VALUES(%s, %s);
        """, (input_client_id, input_phonenumber))
        conn.commit()


def change_client_name():
    input_id_for_changing_name = input("Введите id клиента имя которого хотите изменить: ")
    input_name_for_changing = input("Введите имя для изменения: ")
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients_Homework5 SET client_name=%s WHERE id=%s;
        """, (input_name_for_changing, input_id_for_changing_name))
        conn.commit()


def change_client_surname():
    input_id_for_changing_surname = input("Введите id клиента фамилию которого хотите изменить: ")
    input_surname_for_changing = input("Введите фамилию для изменения: ")
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients_Homework5 SET client_surname=%s WHERE id=%s;
        """, (input_surname_for_changing, input_id_for_changing_surname))
        conn.commit()


def change_client_email():
    input_id_for_changing_email = input("Введите id клиента e-mail которого хотите изменить: ")
    input_email_for_changing = input("Введите e-mail для изменения: ")
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients_Homework5 SET client_email=%s WHERE id=%s;
        """, (input_email_for_changing, input_id_for_changing_email))
        conn.commit()


def change_client_phonenumber():
    input_phonenumber_you_wanna_change = input("Введите номер телефона который Вы хотите изменить: ")
    input_phonenumber_for_changing = input("Введите новый номер телефона, который заменит собой старый: ")
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_phonenumbers SET client_phonenumber=%s WHERE client_phonenumber=%s;
        """, (input_phonenumber_for_changing, input_phonenumber_you_wanna_change))
        conn.commit()


def delete_client_phonenumber():
    input_id_for_deleting_phonenumber = input("Введите id клиента номер телефона которого хотите удалить: ")
    input_phonenumber_for_deleting = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phonenumbers WHERE client_id=%s AND client_phonenumber=%s
        """, (input_id_for_deleting_phonenumber, input_phonenumber_for_deleting))
        conn.commit()


def delete_client():
    input_id_for_deleting_client = input("Введите id клиента которого хотите удалить: ")
    input_client_surname_for_deleting = input("Введите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phonenumbers WHERE client_id=%s
        """, (input_id_for_deleting_client,))
        cur.execute("""
        DELETE FROM clients_Homework5 WHERE id=%s AND client_surname=%s
        """, (input_id_for_deleting_client, input_client_surname_for_deleting))
        conn.commit()



def find_client():
    input_name_for_finding = input("Введите имя для поиска информации о клиенте: ")
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id, client_surname, client_email, client_phonenumber
        FROM clients_Homework5 AS ch5
        LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = ch5.id
        WHERE client_name=%s
        """, (input_name_for_finding,))
        print(cur.fetchall())


def check_function():
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM clients_Homework5;
        """)
        pprint(cur.fetchall())
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_phonenumbers;
        """)
        pprint(cur.fetchall())


def main():
    while True:
        command_symbol = input("\nВведите команду: ")
        if command_symbol == "0":
            create_tables()
        elif command_symbol == "1":
            add_new_client()
        elif command_symbol == "2":
            add_new_phonenumber()
        elif command_symbol == "3":
            change_client_name()
        elif command_symbol == "4":
            change_client_surname()
        elif command_symbol == "5":
            change_client_email()
        elif command_symbol == "6":
            change_client_phonenumber()
        elif command_symbol == "7":
            delete_client_phonenumber()
        elif command_symbol == "8":
            delete_client()
        elif command_symbol == "9":
            find_client()
        else:
            print("\nВы ввели неверный символ, пожалуйста, повторите ввод следуя вышеобозначенным указаниям")

main()

conn.close()