package device

import (
	"net"
)

type Device struct {
	ClientID string
	DeviceID []byte
	Conn     net.Conn
}

func (d *Device) IsValid() bool {
	return d.Conn != nil && len(d.ClientID) > 0 && len(d.DeviceID) > 0
}
