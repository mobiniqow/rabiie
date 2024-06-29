from message_broker.consumer.strategy.models.connectivity import ConnectivityStrategy
from message_broker.consumer.strategy.models.get_server_time import ServerTimeStrategy
from message_broker.consumer.strategy.models.schedule import ScheduleStrategy
from message_broker.consumer.strategy.models.settings import SettingsStrategy
from message_broker.gateway.gateway import GateWay
from message_broker.gateway.gateway_abs import GatewayAbs
from message_broker.message_broker.rabbit_mq.consumer.backend_consumer import BackendConsumer
from message_broker.message_broker.rabbit_mq.consumer.callback.backend_callback import BackendCallBack
from message_broker.message_broker.rabbit_mq.rabbit_mq import RabbitMq

if __name__ == '__main__':
    gateway: GatewayAbs = GateWay()
    gateway.add_strategy(SettingsStrategy())
    gateway.add_strategy(ServerTimeStrategy())
    gateway.add_strategy(ScheduleStrategy())
    gateway.add_strategy(ConnectivityStrategy())
    rabbit = RabbitMq("localhost", 5672, "guest", "guest", "/")
    channel = rabbit.get_channel()
    observer = BackendCallBack(gateway)
    BackendConsumer(channel, observer, "backend_routing_key", "backend_exchange", "backend_queue")
    rabbit.start()
