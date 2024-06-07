package try_job

import (
	"bytes"
	"encoding/hex"
	"fmt"
	"github.com/go-kit/kit/log"
	"iot/device"
	"iot/message"
	"iot/utils"
	"net"
	"time"
)

// period time between users period job
const PERIOD = 100 * time.Millisecond

var JOB_QUEUE = 0

const Name = "OB"
const CODE = 0xFAFA

type TryJob struct {
	TryNumber int8
	SleepTime time.Duration
	Jobs      map[string]Job
	Logger    log.Logger
}

// todo bayad ersal konam va sare har ersal ye shomare bezanam va vaghty packet ersal shode hast va dobare ersal kard
// todo betone packet ro dobare ersal kona az counter 0 beshe
// todo check konam agevice to device manager nist job ro pak konam
func (c *TryJob) findJobWithSequence(code []byte) *Job {
	for _, job := range c.Jobs {
		if bytes.Equal(code, job.Code) {
			return &job
		}
	}
	return nil
}
func (c *TryJob) Controller() {
	go func() {
		for {
			for k, v := range c.Jobs {
				if v.State == SUSPENDED {
					dm := device.GetInstanceManagerWithoutLogger()
					job := c.Jobs[k]
					job.MessageTryNumber = job.MessageTryNumber + 1
					c.Jobs[k] = job
					_device, err := device.GetInstanceManagerWithoutLogger().GetDeviceByConnection(v.Conn)
					if err != nil {
						c.Logger.Log("device not found", v.Conn.RemoteAddr().String())
						continue
					}
					dm.SendMessage(_device, &job.Data)
					if job.MessageTryNumber >= c.TryNumber {
						job.State = END
						c.Jobs[k] = job
						// inja shayad end haro pak konam
					}
				}
			}
			time.Sleep(c.SleepTime)
			//print("Sleep time: ", c.SleepTime, "Seconds", "\n")
		}
	}()
}

func (c *TryJob) Output(con *net.Conn, data *message.Message) error {
	key := utils.JobKeyGenerator(*con, *data)
	_, ok := c.Jobs[key]
	if ok {
		messageCode := fmt.Sprintf("%04X%02X", c.Jobs[key].Code, c.Jobs[key].MessageTryNumber)
		hex, _ := hex.DecodeString(messageCode)
		extention := message.Extention{Name: Name, Code: hex, Length: 10}
		data.Extentions = append(data.Extentions, extention)
	} else {
		JOB_QUEUE++
		println(JOB_QUEUE)
		sequenceNumber, _ := utils.IntToByteArray(JOB_QUEUE)
		job := Job{
			Conn:             *con,
			Data:             *data,
			Code:             sequenceNumber,
			MessageTryNumber: 0,
			TimeCounter:      c.SleepTime,
			State:            SUSPENDED,
		}
		c.Jobs[key] = job
		messageCode := fmt.Sprintf("%04X%02X", job.Code, job.MessageTryNumber)

		hex, _ := hex.DecodeString(messageCode)
		extention := message.Extention{Name: Name, Code: hex, Length: 10}
		data.Extentions = append(data.Extentions, extention)
	}
	return nil
}

func (c *TryJob) Input(con *net.Conn, data *message.Message) error {
	if bytes.Equal(data.Type, message.JOBS) {
		messageCode := data.Payload[:2]
		sequenceNumber := data.Payload[2:]
		c.Logger.Log("message code", messageCode, "sequence number", sequenceNumber)
		job := c.findJobWithSequence(messageCode)
		if job != nil {
			key := utils.JobKeyGenerator(*con, job.Data)
			j := c.Jobs[key]
			j.State = SUCCESS
			c.Jobs[key] = j
		}
		// check shavad ke payam baraye in user hast ya na
	}
	return nil
}
