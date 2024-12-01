import dockerBot

dockerBot.send_message_to_bot("Hello from docker")

markdown_list = [
    "# Header",
    "|| Spoiler ||",
    "-# Subtext"
]

for i in markdown_list:
    dockerBot.send_message_to_bot(i)

num = 0
while num < 10:
    num += 1
    dockerBot.send_message_to_bot(str(num))