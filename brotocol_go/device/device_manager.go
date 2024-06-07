package device

import (
	"bytes"
	"errors"
	"fmt"
	"github.com/go-kit/kit/log"
	"iot/message"
	"iot/middlerware"
	"iot/utils"
	"net"
	"sync"
)

type Manager struct {
	Devices     []Device
	Logger      log.Logger
	Middlewares middlerware.Middlewares
	decoder     message.Decoder
}

var instance *Manager
var one sync.Once

func GetInstanceManager(logger log.Logger) *Manager {

	if instance == nil {
		one.Do(func() {
			instance = &Manager{
				Devices:     make([]Device, 0),
				Logger:      logger,
				Middlewares: *middlerware.GetMiddlewareInstance(),
				decoder: message.Decoder{
					Logger: logger,
				},
			}
		})
	}
	return instance
}
func GetInstanceManagerWithoutLogger() *Manager {
	return instance
}
func (c *Manager) Add(device Device) error {
	for _, element := range c.Devices {
		if element.ClientID == device.ClientID || element.Conn == device.Conn {
			return errors.New("Device is already exist")
		}
	}
	c.Logger.Log("Adding new device with clientID: ", device.ClientID)
	c.Devices = append(c.Devices, device)
	return nil
}
func (c *Manager) GetDeviceByDeviceId(deviceId string) (Device, error) {
	for _, element := range c.Devices {
		if bytes.Equal(element.DeviceID, []byte(deviceId)) {
			return element, nil
		}
	}
	return Device{}, errors.New("Device not exist")
}
func (c *Manager) GetDeviceByConnection(_con net.Conn) (Device, error) {
	for _, element := range c.Devices {
		if _con == element.Conn {
			return element, nil
		}
	}
	return Device{}, errors.New("Device not exist")
}
func (c *Manager) Delete(device Device) error {
	var selectedDevice int = -1
	for index, element := range c.Devices {
		if element.ClientID == device.ClientID || element.Conn == device.Conn || bytes.Equal(element.DeviceID, device.DeviceID) {
			selectedDevice = index
			break
		}
	}
	if selectedDevice == -1 {
		return errors.New("Device not exist")
	}
	c.Logger.Log("Delete device with client_id", device.ClientID)
	c.Devices = append(c.Devices[:selectedDevice], c.Devices[selectedDevice+1:]...)

	return nil
}

func (c *Manager) Update(device Device) error {
	var isExist = false
	for key, element := range c.Devices {
		if element.ClientID == device.ClientID {
			updatedDevice := c.Devices[key]
			updatedDevice = device
			c.Devices[key] = updatedDevice
			isExist = true
			break
		}
	}
	if !isExist {
		return errors.New("device is not exist")
	}
	c.Logger.Log("Updated device with client_id %s", device.ClientID)
	return nil
}

func (c *Manager) Get(device Device) (Device, error) {
	for _, element := range c.Devices {
		if element.ClientID == device.ClientID || element.Conn == device.Conn || bytes.Equal(element.DeviceID, device.DeviceID) {

			return element, nil
		}
	}
	c.Logger.Log("Get device with client_id %s", device.ClientID)
	return device, errors.New("device not exist")
}

//func (c *Manager) SendMessage(conn net.Conn, message []byte) error {
//	data := make(map[string]string)
//	data["content"] = string(message)
//	_, err := c.Middlewares.Output(conn, &data)
//	if err != nil {
//		return err
//	}
//	content := utils.ContentMaker(data)
//	conn.Write([]byte(content))
//	return nil
//}

func (c *Manager) SendMessage(device Device, _message *message.Message) error {
	fmt.Printf("_message.Type %s ,_message.Payload %s\n", _message.Type, _message.Payload)
	_, err := c.Middlewares.Output(device.Conn, _message)
	if err != nil {
		return err
	}
	content := utils.ContentMaker(*_message)
	device.Conn.Write([]byte(content))
	return nil
}

func (c *Manager) SendMessageWithDeviceId(deviceId string, _message message.Message) error {

	device, err := c.GetDeviceByDeviceId(deviceId)
	if err != nil {
		return err
	}
	c.SendMessage(device, &_message)
	return nil
}
