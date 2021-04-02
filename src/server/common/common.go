package common

import (
	"fmt"
	"time"
)

func GetFormattedTime() string {
	return fmt.Sprintf("Time: %s", time.Now().Format("2006-01-02T15:04:05.000Z"))
}
