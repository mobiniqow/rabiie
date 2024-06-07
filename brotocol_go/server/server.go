package server

import (
	"fmt"
	"iot/device"
	"iot/message"
	"iot/message_broker/rabbitmq"
	"iot/middlerware"
	"iot/middlerware/try_job"
	"iot/server/handler"
	"net"

	"github.com/go-kit/kit/log"
)

type server struct {
	Port          int
	middlewares   middlerware.Middlewares
	logger        log.Logger
	messagebroker rabbitmq.MessageBroker
}

func New(port int, logger log.Logger, middlerware middlerware.Middlewares, messageBroker rabbitmq.MessageBroker) *server {
	return &server{
		Port:          port,
		middlewares:   middlerware,
		logger:        logger,
		messagebroker: messageBroker,
	}
}

func (c *server) Run() {
	for _, middleware := range c.middlewares.Middleware {
		middleware.Controller()
	}

	listener, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", c.Port))
	if err != nil {
		c.logger.Log("Error", err)
		return
	}

	if err != nil {
		c.logger.Log("Error:", err)
		return
	}
	defer listener.Close()
	defer c.logger.Log("server shutdown")
	// fmt.Println("Server is listening on port 8080")
	c.logger.Log("Server is listening on port 8080")

	deviceManager := device.GetInstanceManager(c.logger)

	validator := message.Validator{}

	decoder := message.Decoder{Logger: c.logger}
	// rabbit mq consumer run
	go c.messagebroker.Run()
	for {
		// Accept incoming connections
		conn, err := listener.Accept()
		if err != nil {
			c.logger.Log("Error:", err)
			continue
		}
		newDevice := device.Device{Conn: conn, ClientID: conn.RemoteAddr().String()}

		deviceManager.Add(newDevice)
		handler := handler.Handler{Connection: conn, DeviceManager: deviceManager, Logger: c.logger,
			Validator: validator, Decoder: decoder, Device: newDevice, Middleware: &c.middlewares,
			MessageBroker: rabbitmq.NewMessageBroker("amqp://guest:guest@localhost", c.logger)}
		handler.Start()
	}
}

func (c *server) Use(middleware try_job.TryJob) {
	c.middlewares.Add(&middleware)
}
