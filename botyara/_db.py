# Когда-нибудь возможно пригоидтся, пусть будет
# if chat_id != "": # Необходимо вставить chat_id
#     table = """
#     CREATE TABLE IF NOT EXISTS user_messages(
#         username TEXT,
#         message TEXT,
#         date_message TEXT
#     )
#     """
# else:
#     table = """
#     CREATE TABLE IF NOT EXISTS user_messages(
#         username TEXT,
#         message TEXT,
#         date_message TEXT
#     )
#     CREATE TABLE IF NOT EXISTS kaiten_tasks(
#         username TEXT,
#         tasks TEXT,
#         date TEXT
#     )
#     """