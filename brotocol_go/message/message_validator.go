package message

type Validator struct {
}

func (v *Validator) Validate(body []byte) bool {
	// hadeaghal status dashte bashe
	msg := string(body)
	return len(msg) >= 2
}
