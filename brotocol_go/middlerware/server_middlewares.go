package middlerware

import (
	"fmt"
	"iot/message"
	"net"
	"sync"
)

type Middlewares struct {
	Middleware []Middleware
}

var ones sync.Mutex
var instance *Middlewares

func GetMiddlewareInstance() *Middlewares {
	ones.Lock()
	defer ones.Unlock()
	if instance == nil {
		instance = &Middlewares{
			Middleware: make([]Middleware, 0),
		}
	}
	return instance
}

func (m *Middlewares) Add(middleware Middleware) {
	m.Middleware = append(m.Middleware, middleware)
}

func (m *Middlewares) Inputs(con net.Conn, data *message.Message) (c net.Conn, err error) {
	fmt.Printf("data.Payload %s \n", data.Payload)
	for _, m2 := range m.Middleware {
		m2.Input(&con, data)
	}
	return con, err

}

func (m *Middlewares) Output(con net.Conn, data *message.Message) (c net.Conn, err error) {

	for _, m2 := range m.Middleware {
		m2.Output(&con, data)
	}
	return con, err
}
