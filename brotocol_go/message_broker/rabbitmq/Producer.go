package rabbitmq

import (
	"encoding/json"
	"fmt"
	"github.com/go-kit/kit/log"
	"github.com/wagslane/go-rabbitmq"
	"iot/message"
	"iot/utils"
)

type Producer struct {
	Queue      string
	Exchange   string
	RoutingKey string
	Logger     log.Logger
}

func (c *Producer) SendMessage(deviceID string, message message.Message) error {
	fmt.Printf("Sending message to deviceID: %s, message: %s\n", deviceID, message)
	conn, err := rabbitmq.NewConn(
		"amqp://guest:guest@localhost",
		rabbitmq.WithConnectionOptionsLogging,
	)
	if err != nil {
		c.Logger.Log(err)
	}
	defer conn.Close()
	publisher, err := rabbitmq.NewPublisher(
		conn,
		rabbitmq.WithPublisherOptionsLogging,
		rabbitmq.WithPublisherOptionsExchangeName(c.Exchange),
		rabbitmq.WithPublisherOptionsExchangeDeclare,
	)
	if err != nil {
		c.Logger.Log(err)
	}
	defer publisher.Close()
	messageJson := make(map[string]string)
	messageJson["device_id"] = deviceID
	if len(string(message.Payload)) > 0 {
		messageJson["payload"] = utils.HexToBinary(fmt.Sprintf("%X", string(message.Payload)))
	} else {
		messageJson["payload"] = ""
	}
	if len(string(message.Date)) > 0 {
		messageJson["datetime"] = string(message.Date)
	} else {
		messageJson["datetime"] = ""
	}
	messageJson["type"] = string(message.Type)
	fmt.Printf("messageJson[\"type\"] %s", messageJson["type"])
	fmt.Printf("messageJson  %s", messageJson)
	b, err := json.Marshal(messageJson)
	if err != nil {
		panic(err)
	}
	err = publisher.Publish(
		// inja status ro bapayload ezafekarda var dar ebtedash device id ro dadam => devoceId:type+payload
		b,
		[]string{c.RoutingKey},
		rabbitmq.WithPublishOptionsContentType("application/json"),
		rabbitmq.WithPublishOptionsExchange(c.Exchange),
	)
	if err != nil {
		c.Logger.Log(err)
	}
	return nil

}
