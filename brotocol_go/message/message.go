package message

type Type []byte

var (
	GET_ID      Type = []byte("VV") // 5656
	JOBS        Type = []byte("CD") // 4344
	LAST_STATE  Type = []byte("DD") // 4444
	SERVER_TIME Type = []byte("ST") // 5354
	SCHEDULE    Type = []byte("SD") // 5344
	//ORDER    Type = []byte("CC") // 4343
	//SCHEDULE Type = []byte("CB") // 4342
)

// this extentions for middlewares added data to Main Message payloads

type Message struct {
	Payload    []byte
	Type       Type
	Date       []byte
	Extentions []Extention
}

func NewMessage(_type, datetime, payload []byte) *Message {
	return &Message{Payload: payload, Type: _type, Extentions: make([]Extention, 0), Date: datetime}
}
