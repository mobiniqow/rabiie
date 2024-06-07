package main

import (
	"bufio"
	"fmt"
	"github.com/go-kit/kit/log"
	"iot/device"
	"iot/message"
	"iot/message_broker/rabbitmq"
	"iot/middlerware"
	"iot/middlerware/try_job"
	"iot/server"
	"os"
	"time"
)

func main() {
	PORT := 8080
	var logger log.Logger
	{
		logger = log.NewLogfmtLogger(os.Stderr)
		logger = log.NewSyncLogger(logger)
		logger = log.With(logger, "service", "url", "iot_server", log.DefaultTimestampUTC, "caller", log.DefaultCaller)
	}

	middlerware := middlerware.GetMiddlewareInstance()

	middlerware.Add(&try_job.TryJob{
		TryNumber: 30,
		SleepTime: 10 * time.Second,
		Jobs:      make(map[string]try_job.Job),
		Logger:    logger,
	})

	messagebroker := rabbitmq.NewMessageBroker("amqp://guest:guest@localhost", logger)
	tcpServer := server.New(PORT, logger, *middlerware, messagebroker)

	go func() {
		for {
			reader := bufio.NewReader(os.Stdin)
			fmt.Print("Enter text: ")
			data, _ := reader.ReadString('\n')
			dm := device.GetInstanceManagerWithoutLogger()
			decoder := message.Decoder{Logger: logger}
			_type, payload, datetime, err := decoder.Decoder([]byte(data))
			if err != nil {

			}
			message := message.Message{
				Extentions: make([]message.Extention, 0),
				Type:       _type,
				Payload:    payload,
				Date:       datetime,
			}
			dm.SendMessage(dm.Devices[0], &message)
		}
	}()

	tcpServer.Run()
}
