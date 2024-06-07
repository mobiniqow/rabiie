package handler

import (
	"bytes"
	"fmt"
	"iot/device"
	"iot/message"
	"iot/message_broker/rabbitmq"
	"iot/middlerware"
	"net"

	"github.com/go-kit/kit/log"
)

// in baraye handle kardane yek device khase na hameye device ha
type Handler struct {
	Connection    net.Conn
	Logger        log.Logger
	DeviceManager *device.Manager
	Device        device.Device
	Validator     message.Validator
	Decoder       message.Decoder
	Middleware    *middlerware.Middlewares
	MessageBroker rabbitmq.MessageBroker
}

func (c *Handler) CloseConnection(Connection net.Conn) {
	err := Connection.Close()
	if err != nil {
		c.Logger.Log("Connection closed with error: %v", err)
		panic(err)
	} else {
		c.Logger.Log("Connection closed")
	}
	c.DeviceManager.Delete(c.Device)
}

func (c *Handler) Start() {
	go func() {
		defer c.CloseConnection(c.Connection)
		// buffer for reading data from socket

		for {
			buffer := make([]byte, 1024)
			n, err := c.Connection.Read(buffer)
			if err != nil {
				c.Logger.Log("error from reading data %s from socket: %v", err, c.Connection)
			} else {
				body := buffer[:n]
				_type, payload, datetime, err := c.Decoder.Decoder(body)
				msg := message.NewMessage(_type, datetime, payload)
				if c.Validator.Validate(body) {
					if err != nil {
						c.Logger.Log("error from reading data %s from socket: %v", err, c.Connection)
					} else {
						// agar payami ke amad moshabeh id bod ono add konam be device haie mojod
						if bytes.Equal(_type, message.GET_ID) {
							c.Device.DeviceID = payload
							c.DeviceManager.Update(c.Device)
							c.Logger.Log("Received message with ID:", c.Device.DeviceID)
						} else {
							if c.Device.IsValid() {
								fmt.Printf("new_device.DeviceID %s \n", string(c.Device.DeviceID))
								c.MessageBroker.SendData(string(c.Device.DeviceID), *msg)
								print("yes bro")
							}
						}
					}
				}

				if err != nil {
					c.Logger.Log("error from reading data %s from socket: %v", err, c.Connection)
				} else {
					_, err := c.Middleware.Inputs(c.Connection, msg)
					if err != nil {
						c.Logger.Log("Get message with error: %v", err)
						return
					}
				}
			}
		}
	}()
}
