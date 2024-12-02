import relayService

relayService.send_message_to_server("Hello from docker")

markdown_list = [
    "# Header",
    "|| Spoiler ||",
    "-# Subtext"
]

for i in markdown_list:
    relayService.send_message_to_server(i)

num = 0
while num < 10:
    num += 1
    relayService.send_message_to_server(str(num))