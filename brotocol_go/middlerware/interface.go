package middlerware

import (
	"iot/message"
	"net"
)

type Middleware interface {
	Controller()
	Output(*net.Conn, *message.Message) error
	Input(*net.Conn, *message.Message) error
}
