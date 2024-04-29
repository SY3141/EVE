#handles self bot startup and authentication along with message handling
import discum
import os
from server import keep_alive
from query import query  #, toxicClassify
from assistant import generate_response
from loadBalancer import LoadBalancer

TOKEN = os.environ['TOKEN3']
bot = discum.Client(token=str(TOKEN), log=False)
balancer = LoadBalancer(5)  #load balancer to LLM models
bot.gateway.clearCommands()


@bot.gateway.command
def event(resp):  #called when an http request is received
  message = resp.parsed.auto()
  if resp.event.message:
    payload = message['content']
    print(payload)
    if message['author']['id'] == "742542900470218802" or len(payload) <= 1:
      return  #ignores own messages and empty messages

    elif payload[0] == ".":
      '''toxicResponse = toxicClassify(payload)[0][0]
      if toxicResponse["label"] == "toxic" and toxicResponse["score"] > 0.9:
        reply = "Ignoring toxicity, confidence : " + str(
          round(toxicResponse["score"], 4))
      else:'''
      reply = generate_response(message['content'][1:], balancer.balance())
      print(message["channel_id"])
      bot.sendMessage(message["channel_id"], reply)
    elif "<@742542900470218802>" in message[
        "content"] or "guild_id" not in message:
      #checks for pings to EVE or dms
      payload = payload.replace("<@742542900470218802>", 'Eve')
      response = query(payload)
      print(response)
      bot_response = response['generated_text']
      if not bot_response:  #error in loading huggingface model
        if 'error' in response:
          bot_response = '`Error: {}`'.format(response['error'])
        else:
          bot_response = 'Hmm... something is not right.'
      bot.sendMessage(message['channel_id'], bot_response)


keep_alive()
bot.gateway.run(auto_reconnect=True)
