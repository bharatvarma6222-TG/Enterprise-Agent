from queue import Queue

subscribers = []


def publish(event_type: str, message: str, data=None):

    print(f"PUBLISH: {event_type} -> subscribers={len(subscribers)}")

    event = {
        "type": event_type,
        "message": message,
        "data": data,
    }

    for queue in subscribers:
        queue.put(event)


def subscribe():

    queue = Queue()

    subscribers.append(queue)

    print(f"SUBSCRIBE -> subscribers={len(subscribers)}")

    return queue


def unsubscribe(queue):

    if queue in subscribers:
        subscribers.remove(queue)

    print(f"UNSUBSCRIBE -> subscribers={len(subscribers)}")
