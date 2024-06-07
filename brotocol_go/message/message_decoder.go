package message

import (
	"bytes"
	"errors"
	"fmt"
	"github.com/go-kit/kit/log"
)

type Decoder struct {
	Logger log.Logger
}

func (dec *Decoder) Encoder(message Message) []byte {
	dec.Logger.Log("Encode message:", message)
	_type := message.Type
	payload := message.Payload
	template := fmt.Sprintf("%x%x", _type, payload)
	return []byte(template)
}

//func (dec *Decoder) Decoder(bytes []byte) (string, string, error) {
//	dec.Logger.Log("Decoder bytes:", bytes)
//
//	_type := string(bytes[:2])
//	payload := string(bytes[2:])
//	return _type, payload, nil
//}

func (dec *Decoder) Decoder(data []byte) (_type Type, payload []byte, datetime []byte, err error) {
	fmt.Printf("stirngdata %s\n", data)
	if len(data) < 2 {
		return Type{}, nil, nil, errors.New("message too short")
	}

	_type = data[:2]
	if bytes.Equal(_type, JOBS) {
		return _type, data[2:4], data[4:], nil
	} else if bytes.Equal(_type, GET_ID) {
		// dar halate VV mikhad device id ro befreste device id 11 raghami hastesh

		return _type, data[2:13], data[13:], nil
	} else if bytes.Equal(_type, LAST_STATE) {
		return _type, nil, nil, nil
	} else if bytes.Equal(_type, SERVER_TIME) {
		return _type, nil, data[2:], nil
	} else if bytes.Equal(_type, SCHEDULE) {
		return _type, nil, nil, nil
	}
	return _type, data[2:], nil, nil
}
