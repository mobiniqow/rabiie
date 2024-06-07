package try_job

import (
	"iot/message"
	"net"
	"time"
)

type JobState int

// dar ayande mitonim in ro handle konim ke shayad device payam ro khond vali natonest karo anjam bede

const (
	SUSPENDED JobState = iota
	SUCCESS
	FAILED
	END
)

type Job struct {
	Conn             net.Conn
	Data             message.Message
	Code             []byte
	MessageTryNumber int8
	TimeCounter      time.Duration
	State            JobState
}
