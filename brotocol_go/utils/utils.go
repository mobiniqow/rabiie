package utils

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"iot/message"
	"net"
	"strings"
)

func JobKeyGenerator(conn net.Conn, message message.Message) string {
	return fmt.Sprintf("%s:%s%s%s", conn.RemoteAddr().String(), message.Type, message.Payload)
}

func ContentMaker(message message.Message) string {
	extentions := make([]byte, 0)
	for _, extention := range message.Extentions {
		extentions = append(extentions, extention.Code[:]...)
	}
	return fmt.Sprintf("%s%s%X%04X\r\n", message.Type, message.Payload, message.Date, extentions)
}

func ByteArrayToInt(byteSlice []byte) (int, error) {
	return int(binary.BigEndian.Uint64(byteSlice)), nil
}

func StringToMap(data string) map[string]interface{} {
	_data := strings.Replace(data, "'", "\"", -1)
	sec := map[string]interface{}{}
	if err := json.Unmarshal([]byte(_data), &sec); err != nil {
		fmt.Printf("error %v \n", err)
		panic(err)
	}
	return sec
}
