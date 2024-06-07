package rabbitmq

import (
	"github.com/go-kit/kit/log"
	"github.com/wagslane/go-rabbitmq"
)

type Consumer struct {
	Queue      string
	Exchange   string
	RoutingKey string
	Handler    func(rabbitmq.Delivery) rabbitmq.Action
	Logger     log.Logger
}

func (c *Consumer) Run(mq *rabbitmq.Conn) {
	consumer, err := rabbitmq.NewConsumer(
		mq,
		c.Queue,
		rabbitmq.WithConsumerOptionsRoutingKey(c.RoutingKey),
		rabbitmq.WithConsumerOptionsExchangeName(c.Exchange),
		rabbitmq.WithConsumerOptionsExchangeDeclare,
	)

	if err != nil {
		c.Logger.Log(err)
	}
	defer consumer.Close()

	err = consumer.Run(c.Handler)

	if err != nil {
		c.Logger.Log(err)
	}
}

// example of handler
//func(d rabbitmq.Delivery) rabbitmq.Action {
//	log.Printf("consumed: %v", string(d.Body))
//	// rabbitmq.Ack, rabbitmq.NackDiscard, rabbitmq.NackRequeue
//	return rabbitmq.Ack
//}
