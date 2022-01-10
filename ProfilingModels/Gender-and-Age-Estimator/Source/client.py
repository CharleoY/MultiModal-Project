import pika
import json
import os
import warnings
warnings.filterwarnings("ignore")


def main():
    # declare rabbitMQ queue for messages sending
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='messages_queue', durable=True)

    #parse messages from json
    f = open('Resources/input.json', 'r')
    messages = f.read();
    messages = json.loads(messages);

    for i in range(0, messages['messages'].__len__()):
        try:
            message = messages['messages'][i]
            channel.basic_publish(exchange='',
                                  routing_key='messages_queue',
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,
                                  ))
            print(" [x] Sent %r" % message, )

        except:
            print("Some error occured during message processing")

    connection.close()

if __name__ == "__main__":
    os.chdir('../');
    main()
